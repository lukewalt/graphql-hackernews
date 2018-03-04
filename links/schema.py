
import graphene
from graphene_django import DjangoObjectType

from .models import Link
from users.schema import UserType

class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


#defines a mutation class
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    #defines data that is sent to the server
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # mutation method: creates link on the database using the defined data items
    def mutate(self, info, url, description):
        user = info.context.user or None

        link = Link(
            url=url,
            description=description,
            posted_by=user,
        )
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


#creates mutation class with a field to be resolved which points to the mutation defined above
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
