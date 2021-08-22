db = db.getSiblingDB("cody_db");

//Basic Structure of the collection student games's developer 
db.developedGame.insertMany([
    {
        "idGame": "0",
        "gameName": "nombre_Juego",
        "topic": "tema",
        "parameters": [
            {
                "name": "",
                "level": "",
            }
        ],
        "developer":{
            "studentName":"nombre_Estudiante" ,
            "schoolName": "colegio",
        }
    }
]);

//Basic structure of school, students and teachers
db.professor.insertMany([
    {
        "nameProf":"Jimeno",
        "username":"Usuario",
        "password":"Contraseña hash",
        "schools":[
            {
                "schoolName":  "NombreColegio"
            },  
        ]
    }
]);

//Basic structure of school, students and teachers
db.school.insertMany([
    {
        "idSchool": "",
        "schoolName": "NombreColegio",
        //Basic structure of teachers
        "students": [
            //Basic structure of student player
            {
                "studentName":"Nombre" ,
                "age": "edad",
                "username":"user",
                "password":"haspassword",
            },
        ],
        "associatedGames": [
            {
                "idGame": "",
                "nameGame": "",
            }
        ]
    }
]);
//Structure basic of session's games
db.sessionGame.insertMany([
    {
        "startTime": "",
        "finishTime": "",
        "Game": {
            "idGame": "0",
            "nameGame": "Nombre_Juego",
            "topic": "Tema",
            "score": "value",
            "levels":[
                {
                    "startTime": "",
                    "finishTime": "",
                    "level": "0",
                    "parameters": [
                        {
                            "name":"correctAnswer",
                            "value": "0",
                        },
                        {
                            "name":"incorrectAnswer",
                            "value":  "100",
                        },
                    ]
                }
            ]
        },
        "Student": {
            "username": "diego",
            "school": "col"
        },
    },
]); 

//admin
db.admin.insertMany([
    {
        "name":"Jimeno",
        "username":"Usuario",
        "password":"Contraseña hash",
    }
]);