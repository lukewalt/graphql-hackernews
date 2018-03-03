
import graphene
from graphene_django import DjangoObjectType

from .models import Link


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

    #defines data that is sent to the server
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # mutation method: creates link on the database using the defined data items
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )


#creates mutation class with a field to be resolved which points to the mutation defined above
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
