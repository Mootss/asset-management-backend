
# API for asset management app
A simple server written in Flask to connect [this React app](https://github.com/Mootss/asset-management) to a postgres database (supabase) 

database connection string can be found in app.py

## API Reference

base url: https://moothy.pythonanywhere.com

#### Get all staff

```
  GET /staff
```


#### Get currently assigned assets for a staff

```
  GET /staff/<national_id>/current
```

| Parameter | Type     |Eg.|
| :-------- | :------- | :---|
| `national_id`      | `string` | A003344|

returns array of asset objects


#### Get all assets

```
  GET /assets
```

#### Add a new asset

```
  POST /assets/create
```

#### Update an asset

```
  POST /assets/edit/<id>
```