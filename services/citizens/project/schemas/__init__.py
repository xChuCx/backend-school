schemas = {'import_schema': {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": [
        "citizens"
    ],
    "properties": {
        "citizens": {
            "$id": "#/properties/citizens",
            "type": "array",
            "title": "The Citizens Schema",
            "items": {
                "$id": "#/properties/citizens/items",
                "type": "object",
                "title": "The Items Schema",
                "required": [
                    "citizen_id",
                    "town",
                    "street",
                    "building",
                    "apartment",
                    "name",
                    "birth_date",
                    "gender",
                    "relatives"
                ],
                "properties": {
                    "citizen_id": {
                        "$id": "#/properties/citizens/items/properties/citizen_id",
                        "type": "integer",
                        "title": "The Citizen_id Schema",
                        "default": 0,
                        "examples": [
                            1
                        ]
                    },
                    "town": {
                        "$id": "#/properties/citizens/items/properties/town",
                        "type": "string",
                        "title": "The Town Schema",
                        "default": "",
                        "examples": [
                            "Москва"
                        ],
                        "pattern": "^(.*)$"
                    },
                    "street": {
                        "$id": "#/properties/citizens/items/properties/street",
                        "type": "string",
                        "title": "The Street Schema",
                        "default": "",
                        "examples": [
                            "Льва Толстого"
                        ],
                        "pattern": "^(.*)$"
                    },
                    "building": {
                        "$id": "#/properties/citizens/items/properties/building",
                        "type": "string",
                        "title": "The Building Schema",
                        "default": "",
                        "examples": [
                            "16к7стр5"
                        ],
                        "pattern": "^(.*)$"
                    },
                    "apartment": {
                        "$id": "#/properties/citizens/items/properties/apartment",
                        "type": "integer",
                        "title": "The Apartment Schema",
                        "default": 0,
                        "examples": [
                            7
                        ]
                    },
                    "name": {
                        "$id": "#/properties/citizens/items/properties/name",
                        "type": "string",
                        "title": "The Name Schema",
                        "default": "",
                        "examples": [
                            "Иванов Иван Иванович"
                        ],
                        "pattern": "^(.*)$"
                    },
                    "birth_date": {
                        "$id": "#/properties/citizens/items/properties/birth_date",
                        "type": "string",
                        "format": "date",
                        "title": "The Birth_date Schema",
                        "default": "",
                        "examples": [
                            "26.12.1986"
                        ],
                    },
                    "gender": {
                        "$id": "#/properties/citizens/items/properties/gender",
                        "type": "string",
                        "title": "The Gender Schema",
                        "default": "",
                        "examples": [
                            "male"
                        ],
                        "pattern": "^(.*)$"
                    },
                    "relatives": {
                        "$id": "#/properties/citizens/items/properties/relatives",
                        "type": "array",
                        "title": "The Relatives Schema",
                        "items": {
                            "$id": "#/properties/citizens/items/properties/relatives/items",
                            "type": "integer",
                            "title": "The Items Schema",
                            "default": 0,
                            "examples": [
                                2
                            ]
                        }
                    }
                }
            }
        }
    },
    "additionalProperties": False
},
    'patch_schema': {
        "definitions": {},
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/root.json",
        "type": "object",
        "title": "The Root Schema",
        "anyOf": [
            {"required": ["town"]},
            {"required": ["street"]},
            {"required": ["building"]},
            {"required": ["apartment"]},
            {"required": ["name"]},
            {"required": ["birth_date"]},
            {"required": ["gender"]},
            {"required": ["relatives"]}
        ],
        "properties": {
            "town": {
                "$id": "#/properties/citizens/items/properties/town",
                "type": "string",
                "title": "The Town Schema",
                "default": "",
                "examples": [
                    "Москва"
                ],
                "pattern": "^(.*)$"
            },
            "street": {
                "$id": "#/properties/citizens/items/properties/street",
                "type": "string",
                "title": "The Street Schema",
                "default": "",
                "examples": [
                    "Льва Толстого"
                ],
                "pattern": "^(.*)$"
            },
            "building": {
                "$id": "#/properties/citizens/items/properties/building",
                "type": "string",
                "title": "The Building Schema",
                "default": "",
                "examples": [
                    "16к7стр5"
                ],
                "pattern": "^(.*)$"
            },
            "apartment": {
                "$id": "#/properties/citizens/items/properties/apartment",
                "type": "integer",
                "title": "The Apartment Schema",
                "default": 0,
                "examples": [
                    7
                ]
            },
            "name": {
                "$id": "#/properties/citizens/items/properties/name",
                "type": "string",
                "title": "The Name Schema",
                "default": "",
                "examples": [
                    "Иванов Иван Иванович"
                ],
                "pattern": "^(.*)$"
            },
            "birth_date": {
                "$id": "#/properties/citizens/items/properties/birth_date",
                "type": "string",
                "format": "date",
                "title": "The Birth_date Schema",
                "default": "",
                "examples": [
                    "26.12.1986"
                ],
            },
            "gender": {
                "$id": "#/properties/citizens/items/properties/gender",
                "type": "string",
                "title": "The Gender Schema",
                "default": "",
                "examples": [
                    "male"
                ],
                "pattern": "^(.*)$"
            },
            "relatives": {
                "$id": "#/properties/citizens/items/properties/relatives",
                "type": "array",
                "title": "The Relatives Schema",
                "items": {
                    "$id": "#/properties/citizens/items/properties/relatives/items",
                    "type": "integer",
                    "title": "The Items Schema",
                    "default": 0,
                    "examples": [
                        2
                    ]
                }
            }
        },
        "additionalProperties": False
    }
}
