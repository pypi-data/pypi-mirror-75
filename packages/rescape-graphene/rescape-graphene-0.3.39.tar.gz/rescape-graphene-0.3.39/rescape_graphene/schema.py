import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene import ObjectType, Schema
from graphql_jwt.decorators import login_required, staff_member_required
from rescape_python_helpers import ramda as R

from rescape_graphene.graphql_helpers.schema_helpers import process_filter_kwargs, \
    top_level_allowed_filter_arguments
from rescape_graphene.schema_models.user_schema import UserType, CreateUser, UpdateUser, user_fields


class Query(ObjectType):
    current_user = graphene.Field(
        UserType,
        **top_level_allowed_filter_arguments(user_fields, UserType)
    )

    users = graphene.List(
        UserType,
        **top_level_allowed_filter_arguments(user_fields, UserType)
    )

    @staff_member_required
    def resolve_users(self, info, **kwargs):
        q_expressions = process_filter_kwargs(get_user_model(), kwargs)
        return get_user_model().objects.filter(*q_expressions)

    @login_required
    def resolve_current_user(self, info):
        context = info.context
        user = R.prop_or(None, 'user', context)
        if not user:
            raise Exception('Not logged in!')

        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)
