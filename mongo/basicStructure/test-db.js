db = db.getSiblingDB("testing");

// Create a collection of roles
db.roles.insertMany([
    {
        "name": "admin",
        "description": "Administrator",
        "permission-level": 0,
    },
    {
        "name": "professor",
        "description": "Professor",
        "permission-level": 1,
    },
    {
        "name": "rector",
        "description": "Rector",
        "permission-level": 3,
    }
]);

db.users.insertMany([
    {
        "name": "Jimeno",
        "username": "admin",
        "password": "Contraseña hash",
        "role": "admin",
    },
    {
        "name": "Teacher1",
        "username": "Usurio1",
        "password": "Contraseña",
        "role": "professor",
        "idSchool": 1,
    },
    {
        "name": "Rector",
        "username": "UsuarioRector",
        "password": "Contraseña",
        "role": "rector",
        "idSchool": 1,
    }
]);

//Basic structure of school, students and teachers
db.professors.insertMany([
    {
        "professorNames":"Teacher1",
        "professorSurnames":"aTeacher1",
        "username":"Usuario1",
        "idSchool": 1,
        "courses":[

        ]
    }
]);

db.rectors.insertMany([
    {
        "nameRector":"Rector",
        "surnameRector":"aRector",
        "username":"UsuarioRector",
        "age":30,
        "idSchool": 1,
    }
]);

//Basic structure of school, students and teachers
db.schools.insertMany([
    {
        "idSchool": 1,
        "schoolName": "Test School",
        //Basic structure of teachers
        "students": [
            //Basic structure of student player
            {
                "studentName":"Test Student" ,
                "age": 17
            }
        ],
        "teachers": [
            {
                "professorName" : "Test Professor",
                "age": 30
            }
        ]
    }
]);

//admin
db.admin.insertMany([
    {
        "name":"Jimeno",
        "username":"admin",
    }
]);