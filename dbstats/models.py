from django.db import models


class Countable(models.Model):
    """
    Identifies a model or a SQL query.  A model is identified by app name
    and model name.

    These two specifiers are mutually exclusive:
      {app_name, model_name}
      {sql}

    The sql can be manually written or obtained from a Django QuerySet object
    by stringifying the query attribute of the QuerySet.  A higher-level API
    for doing this is TBD.
    """
    app_name = models.CharField(max_length=200, null=True,
                                help_text='')
    model_name = models.CharField(max_length=200, null=True)
    sql = models.CharField(max_length=10000, null=True,
                           help_text='SQL query relation to count')
    queryset = models.CharField(max_length=10000, null=True,
                                help_text='Serialized un-evaluated QuerySet')


class SnapshotDefinition(models.Model):
    """
    A collection of Countables that can be evaluated to create a Snapshot.

    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    countables = models.ManyToManyField(Countable)


class Snapshot(models.Model):
    """
    A collection of RowCounts at a given point in time.

    A Snapshot is modeled on a SnapshotDefinition.

    A null database_name means the current database.
    """
    database_name = models.CharField(max_length=200, null=True,
                                     help_text='Django database identifier')
    definition = models.Model(SnapshotDefinition)
    label = models.CharField(max_length=200)
    taken = models.DateTimeField()


class RowCount(models.Model):
    """
    Row count for a relation (a table/model or a query).  A RowCount belongs
    to a Snapshot.
    """
    countable = models.ForeignKey(Countable)
    snapshot = models.ForeignKey(Snapshot)
    count = models.BigIntegerField()
