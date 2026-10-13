Models
==============
Status models contain protocol lookup tables. ``Meters``, ``AftStatements``,
``GameFeatures``, and ``Tito`` are instance-owned observation collections.
Unknown fields start as ``None``. Their ``snapshot()`` method includes observed
zero values and returns a read-only copy.

.. toctree::
   :maxdepth: 1
   :caption: Models List
   :name: modelstoc

   models.AftLockStatus
   models.AftReceiptStatus
   models.AftRegistrationStatus
   models.AftStatements
   models.AftTransferStatus
   models.AftTransferType
   models.Denomination
   models.EftStatement
   models.GPoll
   models.GameFeatures
   models.Meters
   models.TitoStatement
