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

### View routes

`/dashboard` - main page to upload documents for classification

`/dashboard/stats` - page to show some info about the dataset and classifier's accuracy

`/dashboard/resolve/{id}` - document resolution page

### API routes

`GET /api/stats` - returns info about the dataset and classifier's accuracy

**Sample response:**

```
{
    "status": "ok",
    "accuracy": 0.9296687543789429,
    "dataset": [
        {
            "name": "APAC",
            "description": "",
            "lobs": [
                {
                    "name": "Commercial Lending",
                    "description": "",
                    "regions": [
                        {
                            "name": "Regulation A",
                            "size": 1202,
                            "description": ""
                        },
                        {
                            "name": "Regulation B",
                            "size": 1,
                            "description": ""
                        },
                        {
                            "name": "Regulation C",
                            "size": 1,
                            "description": ""
                        },
                        {
                            "name": "Regulation D",
                            "size": 1201,
                            "description": ""
                        },
                        {
                            "name": "Unknown",
                            "size": 253,
                            "description": ""
                        }
                    ],
                    "size": 2658
                },
                {
                    "name": "Consumer Lending",
                    "description": "",
                    "regions": [
                        {
                            "name": "Regulation A",
                            "size": 1201,
                            "description": ""
                        },
                        {
                            "name": "Regulation B",
                            "size": 1,
                            "description": ""
                        },
                        {
                            "name": "Regulation C",
                            "size": 1,
                            "description": ""
                        },
                        {
                            "name": "Regulation D",
                            "size": 1201,
                            "description": ""
                        },
                        {
                            "name": "Unknown",
                            "size": 253,
                            "description": ""
                        }
                    ],
                    "size": 2657
                },
                {
                    "name": "Credit Cards",
                    "description": "",
                    "regions": [
                        {
                            "name": "Regulation A",
                            "size": 1201,
                            "description": ""
                        },
                        {
                            "name": "Regulation B",
                            "size": 1,
                            "description": ""
                        },
                        {
                            "name": "Regulation C",
                            "size": 1,
                            "description": ""
                        },
                        {
                            "name": "Regulation D",
                            "size": 1201,
                            "description": ""
                        },
                        {
                            "name": "Unknown",
                            "size": 253,
                            "description": ""
                        }
                    ],
                    "size": 2657
                },
                {
                    "name": "Unknown",
                    "description": "",
                    "regions": [],
                    "size": 253
                }
            ],
            "size": 10629
        },
        ...
    ]
}
```

`POST /api/doc/classify` - submit documents to classify

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
            "id": 39,
            "resolve_url": "/dashboard/resolve/39",
            "name": "filename1.txt",
            "poc": "Jane Doe <zyx@email.com>",
            "prediction": {
                "region": [
                    {
                        "name": "APAC",
                        "confidence": 0.3076419169255379
                    },
                    {
                        "name": "EMEA",
                        "confidence": 0.3281746616163042
                    },
                    {
                        "name": "NAMR",
                        "confidence": 0.3203650640608659
                    },
                    {
                        "name": "Unknown",
                        "confidence": 0.04381835739729199
                    }
                ],
                "lob": [
                    {
                        "name": "Commercial Lending",
                        "confidence": 0.22169840459798154
                    },
                    {
                        "name": "Consumer Lending",
                        "confidence": 0.22824604024061101
                    },
                    {
                        "name": "Credit Cards",
                        "confidence": 0.2198775299279205
                    },
                    {
                        "name": "Investment Banking",
                        "confidence": 0.21222770972274665
                    },
                    {
                        "name": "Unknown",
                        "confidence": 0.11795031551074026
                    }
                ],
                "category": [
                    {
                        "name": "Regulation A",
                        "confidence": 0.012115129738765362
                    },
                    {
                        "name": "Regulation B",
                        "confidence": 0.00133806780304853
                    },
                    {
                        "name": "Regulation C",
                        "confidence": 0.0012155182462457712
                    },
                    {
                        "name": "Regulation D",
                        "confidence": 0.07633194763560947
                    },
                    {
                        "name": "Unknown",
                        "confidence": 0.9089993365763308
                    }
                ]
            }
        },
        {
            "id": 40,
            "resolve_url": "/dashboard/resolve/40",
            "name": "filename2.txt",
            "poc": "Jane Doe <zyx@email.com>",
            "prediction": {
                "region": [
                    {
                        "name": "APAC",
                        "confidence": 0.31812894917740503
                    },
                    {
                        "name": "EMEA",
                        "confidence": 0.3164168454038309
                    },
                    {
                        "name": "NAMR",
                        "confidence": 0.3238583999468782
                    },
                    {
                        "name": "Unknown",
                        "confidence": 0.04159580547188591
                    }
                ],
                "lob": [
                    {
                        "name": "Commercial Lending",
                        "confidence": 0.22580635098709462
                    },
                    {
                        "name": "Consumer Lending",
                        "confidence": 0.22792568574900077
                    },
                    {
                        "name": "Credit Cards",
                        "confidence": 0.22486355659865048
                    },
                    {
                        "name": "Investment Banking",
                        "confidence": 0.21444968761375421
                    },
                    {
                        "name": "Unknown",
                        "confidence": 0.10695471905149992
                    }
                ],
                "category": [
                    {
                        "name": "Regulation A",
                        "confidence": 0.012288383851908318
                    },
                    {
                        "name": "Regulation B",
                        "confidence": 0.0013455355204019775
                    },
                    {
                        "name": "Regulation C",
                        "confidence": 0.0012221478225105053
                    },
                    {
                        "name": "Regulation D",
                        "confidence": 0.07878998324848564
                    },
                    {
                        "name": "Unknown",
                        "confidence": 0.9063539495566936
                    }
                ]
            }
        }
    ]
}
```

`POST /api/doc/resolve` - resolve document and add it to the dataset

**Sample request:**

```
{
	"id": 12
}
```
