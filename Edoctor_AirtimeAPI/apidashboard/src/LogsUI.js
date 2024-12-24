import { BrowserRouter, Routes, Route } from "react-router-dom";
import  React, { useEffect, useState } from "react";
import DepositsUI from "./pages/DepositsUI";
import WithdrawsUI from "./pages/WithdrawsUI";



function LogsUI()
{
    return(
        
            <Routes>
                <Route path="/" element = {<DepositsUI/>} />
                <Route index element = {<DepositsUI/>} />
                <Route path="/deposits" element = {<DepositsUI/>} />
                <Route path="/withdraws" element = {<WithdrawsUI/>} />
            </Routes>
        
    );
}

export default LogsUI;