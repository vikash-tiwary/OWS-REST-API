import factory

from restapi.models import post

class PostFactory(factory.Factory):
    """Post factory class."""

    class Meta:
        """Meta class representing the post model."""

        model = post.Post

    id = factory.Sequence(lambda n: str(n).zfill(1))
    title = factory.Sequence(lambda n: 'Post title {}'.format(n + 1))
    description = factory.Sequence(lambda n: 'Post description {}'.format(n + 1))
