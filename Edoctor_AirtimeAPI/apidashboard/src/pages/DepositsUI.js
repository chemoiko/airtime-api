import React, {useState} from "react";
import "./styles/deposits.css";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow,Paper, TableFooter, TablePagination } from "@mui/material";

const data_map = 
    [
        {
        "status":"200 success",
        "data": "{}",
        "response":"{}",
        "endpoint":"/airtime/api",
        "date":"3/30/2024"
        },
        {
            "status":"500 failed",
            "data": "{}",
            "response":"{}",
            "endpoint":"/airtime/api/deposits",
            "date":"3/30/2024"
        },
        {
            "status":"500 failed",
            "data": "{}",
            "response":"{}",
            "endpoint":"/airtime/api/deposits",
            "date":"3/30/2024"
        },
        {
            "status":"500 failed",
            "data": "{}",
            "response":"{}",
            "endpoint":"/airtime/api/deposits",
            "date":"3/30/2024"
        },
        {
            "status":"500 failed",
            "data": "{}",
            "response":"{}",
            "endpoint":"/airtime/api/deposits",
            "date":"3/30/2024"
        },
        {
            "status":"500 failed",
            "data": "{}",
            "response":"{}",
            "endpoint":"/airtime/api/deposits",
            "date":"3/30/2024"
        },
        {
            "status":"500 failed",
            "data": "{}",
            "response":"{}",
            "endpoint":"/airtime/api/deposits",
            "date":"3/30/2024"
        }
    ];

function DepositsUI()
{
    const [page_no, setPageno] = useState(0);
    const [items_per_page, setPageItemNo] = useState(10);

    const onPagenoChange = (event,new_page_no)=>{
            setPageno(new_page_no);
    };

    const onItemsnoChange = (event) => {
        const pg_cap = event.target.value;
        
        setPageItemNo(pg_cap);
};
    return (
        <div className = "deposits_main">
            Deposit Logs
            <div className = "deposits_div_main">
                <TableContainer stickyHeader component={Paper} >
                    <Table sx={{ height: '70vh' }}>
                        <TableHead sx={{backgroundColor:"gray"}}>
                            <TableRow >
                                <TableCell sx={{fontWeight:"bold"}}>
                                    Status
                                </TableCell>
                                <TableCell sx={{fontWeight:"bold"}}>
                                    Request Data
                                </TableCell>
                                <TableCell sx={{fontWeight:"bold"}}>
                                    Endpoint
                                </TableCell>
                                <TableCell sx={{fontWeight:"bold"}}>
                                    Response
                                </TableCell >
                                <TableCell sx={{fontWeight:"bold"}}>
                                    Date
                                </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data_map.slice(page_no*items_per_page,(page_no*items_per_page)+items_per_page).map((datum)=>(
                            <TableRow sx={{height:"50px"}}>
                                <TableCell>{datum.status}</TableCell>
                                <TableCell>{datum.data}</TableCell>   
                                <TableCell>{datum.endpoint}</TableCell> 
                                <TableCell>{datum.response}</TableCell>  
                                <TableCell>{datum.date}</TableCell>
                            </TableRow>
                            ))}
                            <TableRow>
                                
                            </TableRow>
                        </TableBody>
                        <TableFooter>
                            <TablePagination
                                rowsPerPageOptions={[0,1,2,5,10]}
                                count={data_map.length}
                                rowsPerPage={items_per_page}
                                page={page_no}
                                onPageChange={onPagenoChange}
                                onRowsPerPageChange={onItemsnoChange}/>
                        </TableFooter>
                    </Table>
                </TableContainer>
            </div>
        </div>
    );
}

export default DepositsUI;