import './App.css';
import './Login.css';
import React,{ Component,useState } from 'react';
import { TextField, Button} from '@mui/material';
import ReactLoading from 'react-loading';


function LoginBtn()
{
    let [btn_click, btnClickFx] = useState(false);

    const onclickFx = ()=>{
        btnClickFx(!btn_click);
            
    };
    
    if(btn_click===false)
    {
        return(
            <Button variant='contained' onClick={onclickFx}>LOGIN IN</Button>
        );

    }
    else
    {
        return (
            <Button variant='contained' onClick={onclickFx}><ReactLoading type="balls" height={"50%"} width={"80%"}/></Button>
        );
    }
}
function LoginViews()
{
    return (
        <div className='login-view'>
            <b>PLEASE LOGIN TO YOUR DASHBOARD</b><br/>
            <TextField className='login-input-field' placeholder='Username'/><br/><br/>
            <TextField className='login-input-field' placeholder='Password' type='password'/><br/><br/>
            <LoginBtn/>
        </div>
    );
}

export function LoginUI()
{
    return (
                <div className="login-div">
                    <LoginViews/>
                </div>
    );
}

export default LoginUI;