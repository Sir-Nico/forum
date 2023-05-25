import React, { useEffect } from "react";

export default function Home() {

    useEffect(() => {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        fetch('/api/get/messages/', {
            'method': 'GET',
            'headers': headers,
        }).then(function(response) {
            console.log(response);
            response.json().then(function(json) {
                const msgList = json.messages
            });
        });
    });

    const TestDatabase = () => {
        console.log("Clicked!");
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        fetch("/api", {
            "method" : "POST",
            "headers": headers,
            "body": JSON.stringify({
                "test": "test"
            })
        }).then(function(response) {
            console.log(response);
            response.json().then(function(json) {
                console.log(json);
            });
        });
    };


    return (
        <div className="h-full z-0">
            <div className="flex justify-center">
                <span className="text-xl font-bold py-5">Det kommer til å se bedre ut jeg lover</span>
            </div>
            <div className="flex justify-center">
                <button onClick={TestDatabase} className="px-2 py-1 bg-gray-200 border border-gray-300 rounded-xl hover:bg-gray-300">API test</button>
            </div>
        </div>
    );
};
