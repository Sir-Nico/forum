import React, { useEffect } from "react";

export default function Home() {
    const userRef = React.useRef();
    const passwordRef = React.useRef();
  
    
    useEffect(() => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        fetch('/api/get/messages/', {
            'method': 'GET',
            'headers': headers,
        }).then(function(response) {
            // console.log(response);
            response.json().then(function(json) {
                const msgList = json.messages;
                console.log(msgList);
                document.getElementById('messageList').innerHTML = ''
                for (let message in msgList) {
                    document.getElementById('messageList').innerHTML += '<li>' + msgList[message] + '</li>';
                };
            });
        });
    });


    const testDatabase = () => {
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        fetch("/api", {
            "method" : "GET",
            "headers": headers,
        }).then(function(response) {
            // console.log(response);
            response.json().then(function(json) {
                console.log(json);
            });
        });
    };


    const createUser = () => {
        const data = {
            username: userRef.current.value,
            password: passwordRef.current.value,
        };
        console.log(data)
        if (data.username === "") {
            console.log("ERROR: No username provided");
            return
        } else if (data.password === "") {
            console.log("ERROR: No password provided");
            return
        } else {
            const headers = new Headers();
            headers.append("Content-Type", "application/json");
            fetch("/api/register", {
                "method" : "POST",
                "headers" : headers,
                "body" : JSON.stringify({
                    "username": data.username,
                    "password": data.password
                })
            }).then(function(response) {
                if (response.ok) {
                    window.location.reload();
                };
            })
        }
    };


    return (
        <div className="h-max w-full">
            <div className="flex justify-center">
                <span className="text-xl font-bold py-5">Det kommer til å se bedre ut jeg lover</span>
            </div>
            <div className="flex justify-center font-bold">
                <span>Meldinger fra Databasen:</span>
            </div>
            <div className='flex justify-center pb-10'>
                <ul id='messageList'></ul>
            </div>
            <div className="flex justify-center">
                <input id="nameInput" placeholder="Brukernavn" ref={userRef} className="bg-gray-100 rounded-lg border border-gray-350"></input>
                <input id="passInput" ph="Passord" ref={passwordRef} type="password" className="bg-gray-100 rounded-lg border border-gray-350"></input>
                <button onClick={createUser} className="px-2 py-1 bg-gray-200 border border-gray-300 rounded-xl hover:bg-gray-300">reg test</button>
            </div>
        </div>
    );
};
