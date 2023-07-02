import { useState } from 'react';
import logo from '../assets/logo.png'
import '../styles/styles.css'
import Banner from './banner';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { DropdownData } from '../data';
import DropdownComponent from './dropdown';


function Hero() {

    const [selectedOption, setSelectedOption] = useState(DropdownData[0]);

    const handleSelectOption = (strikeprice, expdate) => {
        setSelectedOption(strikeprice, expdate);
    };

    return (
        <>

            <div className='banner-main'>

                <Banner />
                <div className='banner-button-area'>
                    <div className='dropdown-left'>
                        {/* Render Data based on the classifications that are made */}
                        <NavDropdown
                            id="nav-dropdown-dark-example"
                            title="NIFTY 50"
                        >

                            <NavDropdown.Item href="#action/3.1">FINNIFTY</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.2">  BANKNIFTY </NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">MIDCPNIFTY</NavDropdown.Item>
                        </NavDropdown>
                    </div>

                    <div className='dropdown-left-2'>
                        <label className='button-label'>Expiry Date</label>

                        {/* Expiry Date Dropdown */}
                        <DropdownComponent
                            strikePrice={DropdownData}
                            selectedOption={selectedOption}
                            onSelectOption={handleSelectOption}
                        />

                        <span className='or'>|</span>

                        <label className='button-label'>Strike Price</label>

                        {/* Strike Price Dropdown */}
                        <DropdownComponent
                            strikePrice={DropdownData}
                            selectedOption={selectedOption}
                            onSelectOption={handleSelectOption}
                        />

                        <span className='or'>|</span>

                        <label className='button-label'>Symbol</label>
                        <NavDropdown
                            id="nav-dropdown-dark-example"
                            // Render the Symbol as in the Dataset
                            title="Select"
                            className='dropdown-2'
                        >
                            <NavDropdown.Item className='dropdown-2' href="#action/3.1">Symbol 1</NavDropdown.Item>
                            <NavDropdown.Item className='dropdown-2' href="#action/3.2">Symbol 2</NavDropdown.Item>
                            <NavDropdown.Item className='dropdown-2' href="#action/3.3">Symbol 3</NavDropdown.Item>
                        </NavDropdown>
                    </div>
                </div>


            </div>
        </>
    );
}

export default Hero;