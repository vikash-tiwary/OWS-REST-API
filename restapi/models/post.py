import sqlalchemy
from sqlalchemy.sql.expression import delete
from restapi.connectors import mysql
from oto import response
class Post(mysql.BaseModel):
    """
    Post model for post table
    id is a primary key
    """
    __tablename__ = 'post'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String(100))
    description = sqlalchemy.Column(sqlalchemy.String(200))

    def to_dict(self):
        """Create a dictionary of this object's post."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description}

    
    def get_post(id):
        """
        Fetch list of post dictionaries

        Returns:
             response.Response: list of post dictionaries
        """
        with mysql.db_session() as session:
            if id:
                post=session.query(Post).get(id)
                if not post:
                    return response.create_not_found_response(
                        'post is not available')

                post_dict=post.to_dict()
            else:
                posts=session.query(Post).all()
                post_dict= [post.to_dict() for post in posts]

            return response.Response(message=post_dict) 


    def create_post(post_data):
        with mysql.db_session() as session:
            title=post_data['title']
            description=post_data['description']
            db_list=['title','description']
            flag=all(k in db_list for k in post_data)
            if not flag :
                return response.Response(message='"error:Please post correct data"')
            
            create_data=Post(title=title,description=description)

            session.add(create_data)
            # flush the session so a new record gets the primary key value
            session.flush()
            data=create_data.to_dict()

        return response.Response(message=data)

    def update_post(post_data,id):
        with mysql.db_session() as session:
            title=post_data['title']
            description=post_data['description']
            db_list=['title','description']
            flag=all(k in db_list for k in post_data)
            if not flag :
                return response.Response(message='"error: Please take correct key"')
            
            post=session.query(Post).get(id)
            if not post:
                return response.Response(message="{id} id not available in data base".format(id=id))
            else:
                post.title=title
                post.description=description
                
                # flush the session so a new record gets the primary key value
                session.flush()
                data=post.to_dict()

        return response.Response(message=data)

    def delete_post(id):
        with mysql.db_session() as session:
            post=session.query(Post).get(id)
            if not post:
                return response.Response(message="{id} id not available in data base".format(id=id))
            else:
                session.delete(post)
                session.flush()

        return response.Response(message={"Post Deleted"})
