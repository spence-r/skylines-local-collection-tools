# skylines-local-collection-tools
A set of Python scripts for local management of Cities:Skylines workshop assets.

- -- 
Currently, the script checks a path on disk (containing your locally stored assets) against the assets belonging to one or more workshop collections. 
Assets are flagged for review if they are contained locally and do not belong to the collection(s), or if there are items in the collection which do not exist locally.

This is performed by downloading the collection page(s) and evaluating the contained items, so the collection(s) must be set to Public visibility or the script will fail.
If necessary, publish the collection and set its visibility to public before executing the script, then return it to private/friends visibility if desired. 

Inside the script, you must edit the local asset path, the list of collections (collection infos), and their corresponding URL and location on disk. The "name" property of the collection info is only used for the local/report output. 

- --
## Future TODOs: 
* Better report output - HTML with clickable links, directly open pages of missing assets, etc
* Local file management - find files in the Workshop folder and move/copy them to the local collection folder, sync local/workshop files
* "Themed" collection management - make it easy to swap out themed/regional collections of assets at will (so I can build two styles of cities at different times without collections headache)
