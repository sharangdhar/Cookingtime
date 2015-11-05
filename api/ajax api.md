# AJAX API

<hr>

## Get


### /search?type=...query=...

#### Return
    
    {
        "type":"type"
        "items":["<div>...</div>","<div>...</div>"]
    }

<hr>

## Post

### General

### Error codes

- "Success"
- "Error"

### Error object

- field_name: error_html

### /post_img

    item_id=...&user_id=...&data=...

- item_id is the id of the food/recipe/equipment
- user_id is the id of the user
- data is the image data
- return
    - error code
        - on failure
            - "error": array of error objects
        - on success
            - "image": html for image

### /post_time

    item_id=...&constant=...

- item_id is the id of the food/recipe/equipment
- constant is the heating constant
- return
    - error code
        - on failure
            - array of error objects
        - on success
            - "constant": new heating constant



###/post_review

    item_id=...&title=...&stars=...&text=...
- return is 
    - error code
        - on error
            - "error": array of error objects
        - on success
            - "post": html of post