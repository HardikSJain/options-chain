import React, { useEffect, useState } from 'react';
import NavDropdown from 'react-bootstrap/NavDropdown';
import '../styles/styles.css';

const API = "http://127.0.0.1:8080/api/symbol_date_option/FINANCIALS+04JUL23";

function DropdownComponent(props) {
    const { strikePrice, expiryDate, selectedOption, onSelectOption } = props;
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(API);
                const jsonData = await response.json();
                console.log("Fetched JSON:", jsonData);

                const strikePriceList = jsonData.strike_price.map((strikePrice) => ({
                    label: strikePrice.toString(),
                    value: strikePrice,
                }));

                setData(strikePriceList);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <>
            <NavDropdown id="nav-dropdown-dark-example" title="Select" className="dropdown-2">
                {data.map((strikePriceItem) => (
                    <NavDropdown.Item
                        key={strikePriceItem.label}
                        className={selectedOption === strikePriceItem.value ? 'selected' : ''}
                        onClick={() => onSelectOption(strikePriceItem.value)}
                    >
                        {strikePriceItem.label}
                    </NavDropdown.Item>
                ))}
            </NavDropdown>
        </>
    );
}

export default DropdownComponent;
