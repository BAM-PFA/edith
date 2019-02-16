#!/usr/bin/env python3

# local imports
from .. models import Data_Source


def main(dataSourceID):
	dataSourceID = int(dataSourceID)
	dataSource = Data_Source.query.get(dataSourceID)

	results = {
		'dataSourceName' : dataSource.dbName,
		'dataSourceLayout' : dataSource.fmpLayout,
		'dataSourceIP' : dataSource.IPaddress,
		'dataSourceUsername' : dataSource.username,
		'dataSourceCredentials' : dataSource.credentials,
		'dataSourcePrimaryID' : dataSource.primaryAssetID,
		'dataSourceSecondaryID' : dataSource.secondaryAssetID
	}

	return results

