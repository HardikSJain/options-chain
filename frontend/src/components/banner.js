import '../styles/styles.css'


function Banner() {
    return (
        <div className='banner-main-text'>
            <text className="banner-text-left">
                Option Chain (Equity Derivatives)
            </text>

            {/* The API will fetch the current underlying NIFTY price over here */}

            <div className='test'>
                <label className='banner-text-right'> Underlying Index: <span className='blue-middle-text'>NIFTY </span>19,586.5</label>

                {/* The API will fetch the current date over here */}

                <label className='sub-text'>
                    As on 30th June, 2023
                </label>
            </div>
        </div>
    )
}

export default Banner