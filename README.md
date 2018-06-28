## RDMT (Hackathon)

### Installation:

1. Clone the repo
2. (Optional) create the Python virtual environment and activate it
3. Go to the directory `rdmt`
4. Execute `pip3 install -r requirements.txt`
5. Execute `python3 manage.py makemigrations rdmt`
6. Execute `python3 manage.py migrate`
7. Execute `python3 manage.py train_model`
8. Execute `python3 manage.py runserver`
9. Now you can access the server at `http://127.0.0.1:8000/`


### Template

HTML templates are available in the directory `/src/templates/dashboard`

### API routes

`POST /api/doc/upload` - upload documents to retrain the classifier

**Sample request:**

```
{
	"ClassA": ["Just a string upload!", "Another string belonging to the class A"]
}
```

**Sample response:**

```
{
    "status": "ok",
    "accuracy": 100,  <-- current accuracy of the model
    "classes": [
        {
            "name": "ClassA",
            "size": 1602,  <-- number of files in the dataset for the class
            "description": ""
        },
        {
            "name": "ClassB",
            "size": 2,
            "description": ""
        },
        {
            "name": "ClassC",
            "size": 1,
            "description": ""
        },
        {
            "name": "ClassD",
            "size": 1600,
            "description": ""
        },
        {
            "name": "ClassUnknown",
            "size": 2500,
            "description": ""
        }
    ]
}
```

`POST /api/doc/classify` - upload documents for classification

**Sample request:**

```
{
	"files": [
        {
            "name": "filename1.txt",
            "text": "Document from a regulator"
        },
        {
            "name": "filename2.txt",
            "text": "Text of a document"
        }
    ]
}
```

**Sample response:**

```
{
    "status": "ok",
    "result": [
        {
            "name": "filename1.txt",
            "prediction": [
                {
                    "class": "ClassA",
                    "confidence": 0.9330803845706523
                },
                {
                    "class": "ClassB",
                    "confidence": 0.0014816925386627777
                },
                {
                    "class": "ClassC",
                    "confidence": 0.0014816925386627777
                },
                {
                    "class": "ClassD",
                    "confidence": 0.023191665821119666
                },
                {
                    "class": "ClassUnknown",
                    "confidence": 0.04076456453090254
                }
            ]
        },
        {
            "name": "filename2.txt",
            "prediction": [
                {
                    "class": "ClassA",
                    "confidence": 0.011837906501410377
                },
                {
                    "class": "ClassB",
                    "confidence": 0.0020274726471681223
                },
                {
                    "class": "ClassC",
                    "confidence": 0.0020274726471681223
                },
                {
                    "class": "ClassD",
                    "confidence": 0.01974377296723903
                },
                {
                    "class": "ClassUnknown",
                    "confidence": 0.9643633752370144
                }
            ]
        }
    ]
}
```
