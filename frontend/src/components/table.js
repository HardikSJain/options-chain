import React, { useEffect, useState } from 'react';
import '../styles/styles.css';

const API = "http://127.0.0.1:8080/api/single_symbol_options/FINANCIALS+2023-07-11";
const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, PATCH, OPTIONS'
};

function OptionTable() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(API, { headers: headers });
                const jsonData = await response.json();
                console.log("Fetched JSON:", jsonData); // Check the fetched JSON response
                console.log("Data:", jsonData); // Check the 'data' property of the response
                setData(jsonData);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();

        const interval = setInterval(fetchData, 1000); // Fetch data every second

        return () => {
            clearInterval(interval); // Clean up the interval when the component unmounts
        };
    }, []);

    if (!data) {
        return <div>Loading...</div>;
    }

    return (
        <div className="table-structure">
            <div className="table-header-1">
                <div className="table-header-text-1">
                    <span>Call (CE)</span>
                    <span>Put (PE)</span>
                </div>
            </div>

            <div className="table-container">
                <table className="table">
                    <thead>
                        <tr>
                            <th>OI</th>
                            <th>OI Qty</th>
                            <th>Volume</th>
                            <th>IV</th>
                            <th>Bid Price</th>
                            <th>Bid Qty</th>
                            <th>LTP</th>
                            <th>LTP +/-</th>
                            <th>Ask Price</th>
                            <th>Ask Qty</th>
                            <th><span className="strike-price">Strike Price</span></th>
                            <th>Bid Price</th>
                            <th>Bid Qty</th>
                            <th>LTP</th>
                            <th>LTP +/-</th>
                            <th>Ask Price</th>
                            <th>Ask Qty</th>
                            <th>IV</th>
                            <th>Volume</th>
                            <th>OI Qty</th>
                            <th>OI</th>
                        </tr>
                    </thead>

                    <tbody>
                        {data.map((item, index) => (
                            <tr key={index}>
                                <td>{item.oi_c}</td>
                                <td>{item.oi_change_c}</td>
                                <td>{item.volume_c}</td>
                                <td>{item.iv_c}</td>
                                <td>{item.bid_c}</td>
                                <td>{item.bidqty_c}</td>
                                <td>{item.ltp_c}</td>
                                <td>{item.change_c}</td>
                                <td>{item.ask_c}</td>
                                <td>{item.askqty_c}</td>
                                <td>{item.strike_price}</td>
                                <td>{item.bid_p}</td>
                                <td>{item.bidqty_p}</td>
                                <td>{item.ltp_p}</td>
                                <td>{item.change_p}</td>
                                <td>{item.ask_p}</td>
                                <td>{item.askqty_p}</td>
                                <td>{item.iv_p}</td>
                                <td>{item.volume_p}</td>
                                <td>{item.oi_change_p}</td>
                                <td>{item.oi_p}</td>
                            </tr>
                        ))}
                    </tbody>

                </table>
            </div>
        </div>
    );
}

export default OptionTable;

