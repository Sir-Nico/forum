import React from "react";
import Home from "../components/Home";
import Header from "../components/Header";
import Footer from "../components/Footer";
import SideNav from "../components/SideNav";


export const HomePage = () => {
    return (
        <div>
            <Header/>
            <div className="flex flex-row">
                <SideNav/>
                <Home/>
            </div>
        </div>
    )
}