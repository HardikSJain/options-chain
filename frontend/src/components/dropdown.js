import NavDropdown from 'react-bootstrap/NavDropdown';
import '../styles/styles.css'

function DropdownComponent(props) {
    const { strikePrice, expiryDate, selectedOption, onselectOption } = props;

    return (
        <><NavDropdown
            id="nav-dropdown-dark-example"
            title="Select"
            className='dropdown-2'
        >
            {strikePrice.map((strikeprice) => (
                <NavDropdown.Item className='dropdown-2'>{strikeprice.label}</NavDropdown.Item>
            ))}

        </NavDropdown>

        </>



    );


}

export default DropdownComponent