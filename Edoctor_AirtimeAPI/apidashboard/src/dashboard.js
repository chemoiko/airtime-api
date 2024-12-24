import React, {Component, useState} from "react";
import './dashboard.css';
import {CiViewBoard} from "react-icons/ci";
import {Button, Box, Select,MenuItem, FormControl, InputLabel} from "@mui/material";
import LogsUI from "./LogsUI";
import { useNavigate } from "react-router-dom";
import { BrowserRouter, Routes, Route } from "react-router-dom";

const nav_map = {
    0: "/deposits",
    1: "/withdraws"
};

const date = new Date().toLocaleDateString('se');
function HeadDiv()
{
    const name = "mrmax";
    return (
        <div className = "dashboard-head-div">
            <center><h2>AIRTIME API Logs DashBoard</h2></center><br/>
            <div className="dashboard-head-div-main">
                <div className = "dashboard-head-div-icon">
                    <div><CiViewBoard size="50px"/></div>
                    <div>{name}<br/>{date}</div>
                </div>
                <div>
                    
                </div>
                <div className = "dashboard-head-div-time">
                    
                </div>
            </div>
        </div>
    );
}

function Navigator()
{
    const  [value , setValue] = React.useState(0);

    const navigator = useNavigate();
    const filterFx = (event)=>{
                            const target_id = event.target.value;
                            setValue(target_id);
                            navigator(nav_map[target_id]);
    };

    return (
        <div>

                    Transaction Category:
                    
                    <FormControl sx={{m:0, minWidth: 200,color:"white"}} size="small">
                        
                        <InputLabel id="dashboard_category">Select Category .... </InputLabel>
                        <Select sx={{m:0,fontSize:"1em",fontFamily:["Courier New"],border:"1px solid black", color:"white"}} labelId = "dashboard_category" label="Category" value={value} onChange={filterFx} MenuProps={{
    sx: {
        
      "&& .Mui-selected": {
        backgroundColor: "blue",
        color:"white"
      }
    }
  }}>
                        
                            <MenuItem sx={{color:"green"}} value={0}>Deposits</MenuItem>
                            <MenuItem value={1}>Withdraw</MenuItem>
                            <MenuItem value={2}>Mini Statements</MenuItem>
                            <MenuItem value={3}>Bank Deposits</MenuItem>
                            <MenuItem value={4}>Bank Withdraw</MenuItem>
                        
                    </Select>

                </FormControl>
                </div>
    );
}
function DashboardUI()
{
    
    return (

        <div className = "dashboard-div">
            <div className = "dashboard-div-main">
                <HeadDiv/>
                <BrowserRouter>
                <Navigator/>
                <div className="main-logs-div">
                    <LogsUI/>
                </div>
                </BrowserRouter>
            </div>
            
        </div>
    );
}

export default DashboardUI;