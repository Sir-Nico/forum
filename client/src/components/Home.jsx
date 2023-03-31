import React from "react";

export default function Home() {

    const TestDatabase = () => {
        console.log("Clicked!")
        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        fetch("/api", {
            "method" : "POST",
            "headers": headers,
            "body": JSON.stringify({
                "test": "test"
            }) // et javascript-object kan vi gjøre til JSON med json-stringify
        }).then(function(response) {
            console.log(response);
            response.json().then(function(json) {
                console.log(json)
            })
        });
    }

    return (
        <div>
        <div className="flex justify-center">
            <span className="text-xl font-bold py-5">Forum</span>
        </div>
            <button onClick={TestDatabase}>API test</button>
        </div>
    );
};
