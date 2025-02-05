
# API for asset management app
A very basic api written in Flask to connect [this React app](https://github.com/Mootss/asset-management) to Supabase (postgres) database

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