# Route Back End:

## User:
|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
| GET    | '/users'| X   |X     |Function to get all the users| |  |{"user":{ "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool }}|
|GET     |'/users/<int:id_user>'|X|X|Return the user specified by its id | id_user: int  | |user :{ "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool }  |
|'POST'| '/users', |X|X| Add an user in the data base|None| { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool } |
 |'PUT'|'/users/<int:id_user>'| |X| Update an user in the data base| id_user: int|  { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str,"is_admin" : bool } |
  |'DELETE'|'/users/<int:id_user>'| |X| | id_user: int ||
  
 ## Offer
 
|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
|GET 	|'/offers' 	|X|X|Function to get all the offers in the database			|			 	||{"offer":{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }} 
|POST	|'/offers/page'|X|X|Function to get a page of the offers 				|none|			 {"nb\_offre": int ,"num\_page":int}  | number of the page, number total of page, a boolean to say if the page is the last, and the list of the offers |
|GET 	|'/offers/<int:id_offer>' 		| |X|Get the offer of id id_offer  					| id_offer: int		  || offer:{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int } 
|POST	|'/offers'|X|X|Function to add an offer in the database	| None| 			{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int } 
|POST|'/offers/link'| |X|Function to add an offer in the database and link it to a field	| None 		|	{ "title" : str, "content" : str, "id\_user" : int, "id\_field" : int, "inbase" : bool } 	
|PUT	|'/offers/<int:id_offer>'		| |X|Function to update an offer				| id_offer :int 	|{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int } 
|DELETE	|'/offers/<int:id_offer>'		| |X|Function to delete an offer					| id_offer :int		
|GET	|'/searchOffersByField/<int:id_field>'	| | |Function to get all the offers who correspond to a field 		| id_field : int 	 none | | {"offer":{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }} 
|GET	|'/searchOffersByUser/<int:id_user>', 	| | |Function to get all the offers who correspond to an user 		| id_user : int 	 none  || {"offer":{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }} | 


## Prediction
|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
|GET	|'/predictions'				|X|X|Function to get all the prediction in the database 		|				 ||{"predictions":{"mark": int, "inbase": bool, "id_offer": int}} 
|GET	|'/predictions/<int:id_offer>'		| |X|Function to get a prediction in the database  			| id_offer: int 	 	||{"predictions":{"mark": int, "inbase": bool, "id_offer": int}} 
|POST	|'/predictions'				|X|X|Function to add a prediction in the database 			| None 	|		{"mark": int, "inbase": bool, "id_offer": int} 
|PUT	|'/predictions/<int:id_prediction>'	|X|X|Function to update a prediction in the database 			|id_prediction :int	|{"mark": int, "inbase": bool,"id_offer": int} 
|DELETE	|'/predictions/<int:id_prediction>'	|X|X|Function to delete a prediction in the database 			| id_prediction : int |
|POST	|'/generatePrediction'			| | |Function to get a prediction from an offer				| None 			 |{ "title" : str, "content" : str } | { "field": { "name": str, "description": str, "descriptor": str, "website": str } } | 
|POST	|'/SaveGeneratePrediction'		| |X|Function to get a prediction from an offer and save it		|None 			| { "title" : str, "content" : str } |{"field": { "name": str, "description": str, "descriptor": str, "website": str }}
|GET	|'/nbPrediction/'			|X|X|Function to get the number of prediction between two date 			|		{"begin\_date": date,"end\_date":date} | none  | int | 
|POST	|'/update\_prediction\_by\_id\_offer'	|X|X|Function to update the prediction corresponding to an offer		|none 	|	 { "id_offer" : int, "id_field" : int }

## Team:
|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
|GET	|'/teams'				|X|X|Function to get all the teams in the database  			|			||{"team":{"id\_prediction": int, "id\_field": int, "nb_members": int}}|
|POST	|'/teams'				| | |Function to add a team in the database 				| None| 			{"id\_prediction": int, "id\_field": int, "nb_members": int} 
|PUT	|'/teams/<int:id_prediction>'		| | |Function to update a team in the database 				| id_prediction :int 	|{"id\_prediction": int, "id\_field": int, "nb_members": int}| 

## Field:
|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
|GET	|'/fields'				|X|X|Function to get all the field in the database  			|			 ||{"fields":{"name": str, "description": str, "descriptor": str,"website": str}} 
|GET	|'/fields/nameonly'			|X|X|Function to get all the field in the database  			|			 ||{"fields":{"id":int, "name": str}}
|GET	|'/fields/<int:id_field>'		| | |Function to get a field in the database  				| id_field: int  	| |{"id": int, "name": str, "description": str, "descriptor": str,"website": str, "contacts":}
|POST	|'/fields'				|X|X|Function to add a field in the database 				| None |			{"name": str, "description": str, "descriptor": str,"website": str, "contacts": [{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}, ...\] } | 
|PUT	|'/fields/<int:id_field>'		|X|X|Function to update a field in the database 			| id_field : int 	|{"name": str, "description": str, "descriptor": str,"website": str} | 
|DELETE	|'/fields/<int:id_field>'		|X|X|Function to delete a field in the database 			| id_field : int 	| 
|GET	|'/searchFieldsByOffer/<int:id_offer>'	| |X|Function to get all the field who correspond to an offer 		| id_offer : int 	| none  | {"fields":{"name": str, "description": str, "descriptor": str,"website": str}} | 

## Contact:
|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
|GET	|'/contacts'				|X|X|Function to get all the contact in the database  			| 			||{"contact":{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}} | 
|GET	|'/contacts/<int:id_contact>'		| |X|Function to get a contact in the database  			| id_contact: int 	 ||{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int} | 
|POST	|'/contacts'				|X|X|Function to add a contact in the database 				| None |			{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int} | 
|PUT	|'/contacts/<int:id_contact>'		|X|X|Function to update a contact in the database 			| id_contact : int |	{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int} | 
|DELETE	|'/contacts/<int:id_contact>'		|X|X|Function to delete a contact in the database			| id_contact : int 	 




## Statistique

|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
|GET	|'/averageMark/'			| | |Function to get the average of the prediction mark between to date 			|{"begin\_date": date,"end\_date":date} | none  | int |
|POST	|'/accuracy'				|X|X|Function to get the accuracy of the system|||int

## Authentification
|Request | Route   |Admin| login|Description|parametres header|param body |return|
|--------|---------|-----|------|--------------|-------------|----|--
|POST	|'/auth/signup'				| | |Function to signup								| None| 		 { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str } | { "token": str, "user": { "email": str, "id": int, "is_admin": boolean, "name": str, "password": str, "role": str, "surname": str } } | 
|POST	|'/auth/login'				| | |Function to login								| None 	|	 { "emailUser" : str, "password" : str} | { "token": str, "user": { "email": str, "id": int, "is_admin": boolean, "name": str, "password": str, "role": str, "surname": str } } |
|POST	|'/auth/logout', 			| |X|Function to logout								| 		{Authorization : Bearer token} | None | { 'result': 'success' } | |
