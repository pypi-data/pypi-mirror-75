import reversion
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import (CharField, ForeignKey)
from safedelete.models import SafeDeleteModel

from rescape_region.models.revision_mixin import RevisionModelMixin


def default():
    return dict(
        # Settings used to generate the sankey. These are required
        settings=dict(
            # The default location for nodes whose location fields is 'NA'
            default_location=[],
            # The column names of the raw data. Used to key columns to meanings
            columns=[],
            # The column name that stores the Sankey stage of the node
            stageKey=None,
            # The column name that stores the value of the node
            valueVey=None,
            # The column name that stores the name of the node
            nodeNameKey=None,
            # Optional color key of the individual node
            nodeColorKey=None,
            # Optional color key of the individual link
            linkColorKey=None,
            # A list of stages. Each stage is a dict with key name and targets array
            # The key is used to list targets in the targes array. The name is the readable name
            # Targets is a list of keys of other stages
            stages=[]
        ),
        # Processed sankey nodes and links. These are generated and readonly
        graph=dict(
            # Nodes are stored by the stage key that they represent
            nodes={},
            link=[]
        ),
        # CSV converted to dicts. Each dict contains column values as indicated in settings.columns
        raw_data=[]
    )


@reversion.register()
class Resource(SafeDeleteModel, RevisionModelMixin):
    """
        Models a resource, such as water
    """
    key = CharField(max_length=50, unique=True, null=False)
    name = CharField(max_length=50, null=False)
    data = JSONField(null=False, default=default)
    # TODO we should probably have models.CASCADE here to delete a resource if the region goes away
    region = ForeignKey('Region', related_name='resources', null=False, on_delete=models.DO_NOTHING)

    class Meta:
        app_label = "rescape_region"

    def __str__(self):
        return self.name
