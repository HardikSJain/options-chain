import React, { useState, useEffect } from 'react';
import NavDropdown from 'react-bootstrap/NavDropdown';
import OptionTable from './table';
import '../styles/styles.css';

const Dropdown = () => {
    const [selectedIndex, setSelectedIndex] = useState('');
    const [selectedExpiry, setSelectedExpiry] = useState('');
    const [selectedStrike, setSelectedStrike] = useState('');
    const [selectedSymbol, setSelectedSymbol] = useState('');
    const [data, setData] = useState([]);
    const apiUrl = 'http://127.0.0.1:8080/api/symbol_date_option/FINANCIALS+04JUL23'; // Update the API endpoint here

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch(apiUrl);
            const jsonData = await response.json();
            setData(jsonData);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const handleIndexChange = (index) => {
        setSelectedIndex(index);
    };

    const handleExpiryChange = (expiry) => {
        setSelectedExpiry(expiry);
        setSelectedIndex(''); // Reset selectedIndex when expiry changes
    };

    const handleStrikeChange = (strike) => {
        setSelectedStrike(strike);
        setSelectedIndex(''); // Reset selectedIndex when strike changes
    };

    const handleSymbolChange = (symbol) => {
        setSelectedSymbol(symbol);
        setSelectedIndex(''); // Reset selectedIndex when symbol changes
    };

    return (
        <div>
            {/* Index */}

            {/* Expiry */}
            <div className='dropdown-left-2'>
                <label className='button-label'>Expiry Date</label>
                <NavDropdown
                    className='dropdown-2'
                    title={selectedExpiry || 'Select'}
                    onSelect={handleExpiryChange}
                >
                    {data.expiry_dates &&
                        data.expiry_dates.map((expiry, index) => (
                            <NavDropdown.Item key={index} eventKey={expiry}>
                                {expiry}
                            </NavDropdown.Item>
                        ))}
                </NavDropdown>
            </div>

            {/* Strike Price */}
            <label className='button-label'>Strike Price</label>
            <NavDropdown
                className='dropdown-2'
                title={selectedStrike || 'Strike Price'}
                onSelect={handleStrikeChange}
            >
                {data.strike_price &&
                    data.strike_price.map((strike, index) => (
                        <NavDropdown.Item key={index} eventKey={strike}>
                            {strike}
                        </NavDropdown.Item>
                    ))}
            </NavDropdown>

            {/* Symbol */}
            <label className='button-label'>Symbol</label>
            <NavDropdown
                className='dropdown-2'
                title={selectedSymbol || 'Symbol'}
                onSelect={handleSymbolChange}
            >
                {data.symbols &&
                    data.symbols.map((symbol, index) => (
                        <NavDropdown.Item key={index} eventKey={symbol}>
                            {symbol}
                        </NavDropdown.Item>
                    ))}
            </NavDropdown>
            {/* <OptionTable selIndex={selectedIndex} selExpiry={selectedExpiry} selStrike={selectedStrike} selSymbol={selectedSymbol}></OptionTable> */}
        </div>
    );
};

export default Dropdown;
