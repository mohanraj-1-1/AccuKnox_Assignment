### 1.Signup<br/>
**Method:** POST<br/>
**URL:** http://localhost:8000/api/signup/<br/>
**Headers:** <br/>
**Content-Type:** application/json<br/>
**Body:** JSON<br/>
{<br/>
    "email": "mohan@raj.com",<br/>
    "password": "password123",<br/>
    "first_name": "Mohan",<br/>
    "last_name": "Raj"<br/>
}<br/>
**Expected Response:** <br/>
{ "message": "User created successfully" }<br/>
![Screenshot 2024-09-10 104858](https://github.com/user-attachments/assets/9ecbe846-d8e2-42c9-89c1-340692dab4c6)<br/>
<br/>
***
### 2. Login<br/>
**Method:** POST<br/>
**URL:** http://localhost:8000/api/login/<br/>
**Headers:** <br/>
**Content-Type:** application/json<br/>
**Body:** JSON<br/>
{<br/>
    "email": "user@example.com",<br/>
    "password": "yourpassword"<br/>
}<br/>
<br/>
**Expected Response:** JSON<br/>
{<br/>
    "message": "Login successful"<br/>
}<br/>
![Screenshot 2024-09-10 105146](https://github.com/user-attachments/assets/e2dd5045-ea5f-48d9-b0ce-a2724650e692)<br/>
<br/>
***
### 3. Search Users<br/>
**Method:** GET<br/>
**URL:** http://localhost:8000/api/search/?search=keyword<br/>
**Headers:**<br/>
**Authorization:** Basic; email and password<br/>
**Query Parameters:** <br/>
**search:** The keyword to search for.<br/>
**Expected Response:** JSON<br/>
{<br/>
    "count": 1,<br/>
    "next": null,<br/>
    "previous": null,<br/>
    "results": [<br/>
        {<br/>
            "id": 1,<br/>
            "email": "user@example.com",<br/>
            "first_name": "FirstName",<br/>
            "last_name": "LastName"<br/>
        }<br/>
    ]<br/>
}<br/>
<br/>
![Screenshot 2024-09-10 105344](https://github.com/user-attachments/assets/059bcacd-33d4-416a-9330-fc409ff074c7)<br/>
<br/>
***
### 4. Send Friend Request<br/>
**Method:** POST<br/>
**URL:** http://localhost:8000/api/friend-request/send/<br/>
**Headers:** <br/>
**Content-Type:** application/json<br/>
**Authorization:** Basic; email and password<br/>
**Body:** JSON<br/>
{<br/>
    "receiver": 2<br/>
}<br/>
<br/>
**Expected Response:** JSON<br/>
{<br/>
    "id": 1,<br/>
    "sender": 1,<br/>
    "receiver": 2,<br/>
    "created_at": "2024-09-10T00:00:00Z",<br/>
    "status": "pending"<br/>
}<br/>
<br/>
![Screenshot 2024-09-10 105500](https://github.com/user-attachments/assets/dda27845-96dc-4885-b3f6-39cfd699c20e)<br/>
<br/>
***
### 5. Respond to Friend Request<br/>
**Method:** POST<br/>
**URL:** http://localhost:8000/api/friend-request/respond/<br/>
**Headers:** <br/>
**Content-Type:** application/json<br/>
**Authorization:** Basic; email and password<br/>
**Body:** JSON<br/>
{<br/>
    "request_id": 1,<br/>
    "action": "accept"  // or "reject"<br/>
}<br/>
<br/>
**Expected Response:** JSON<br/>
{<br/>
    "id": 1,<br/>
    "sender": 1,<br/>
    "receiver": 2,<br/>
    "created_at": "2024-09-10T00:00:00Z",<br/>
    "status": "accepted"  // or "rejected"<br/>
}<br/>
<br/>
![Screenshot 2024-09-10 111759](https://github.com/user-attachments/assets/c407e1eb-81f7-43de-851e-a8c2c7c1df68)<br/>
<br/>
***
### 6. List Friends<br/>
**Method:** GET<br/>
**URL:** http://localhost:8000/api/friends/<br/>
**Headers:** <br/>
**Authorization:** Basic; email and password<br/>
**Expected Response:** JSON<br/>
[<br/>
    {<br/>
        "id": 2,<br/>
        "email": "friend@example.com",<br/>
        "first_name": "Friend",<br/>
        "last_name": "User"<br/>
    }<br/>
]<br/>
<br/>
![Screenshot 2024-09-10 105707](https://github.com/user-attachments/assets/a3c7e4b9-5def-40eb-92ac-c2e60c844f21)<br/>
<br/>
***
### 7. List Pending Friend Requests<br/>
**Method:** GET<br/>
**URL:** http://localhost:8000/api/friend-request/pending/<br/>
**Headers:** <br/>
**Authorization:** Basic; email and password<br/>
**Expected Response:** JSON<br/>
[<br/>
    {<br/>
        "id": 1,<br/>
        "sender": 1,<br/>
        "receiver": 2,<br/>
        "created_at": "2024-09-10T00:00:00Z",<br/>
        "status": "pending"<br/>
    }<br/>
]<br/>
![Screenshot 2024-09-10 111248](https://github.com/user-attachments/assets/b95d380f-45e9-412c-afef-ba8b6410fede)<br/>
<br/>
***
### 8. Limit 3 friend requests within a minute.<br/>
**Method:** POST<br/>
**URL:** http://localhost:8000/api/friend-request/send/<br/>
**Headers:** <br/>
**Content-Type:** application/json<br/>
Authorization: Basic; email and password<br/>
**Body:** JSON<br/>
{<br/>
    "receiver": 2<br/>
}<br/>
<br/>
**Expected Response if Exceeding Limit:** JSON<br/>
{<br/>
    "error": "You cannot send more than 3 friend requests within a minute"<br/>
}<br/>
![Screenshot 2024-09-10 111025](https://github.com/user-attachments/assets/2661e50a-eec6-4bc5-81ad-7ceddfb51426)<br/>
<br/>
**Expected Response if Within Limit:** JSON<br/>
{<br/>
    "id": 1,<br/>
    "sender": 1,<br/>
    "receiver": 2,<br/>
    "created_at": "2024-09-10T00:00:00Z",<br/>
    "status": "pending"<br/>
}<br/>
![Screenshot 2024-09-10 111000](https://github.com/user-attachments/assets/16351379-6e67-4090-b605-c4b970145669)

<br/>
<br/>
<br/>
