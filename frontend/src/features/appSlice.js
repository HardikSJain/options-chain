import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    strikePrice: 0,
    symbol: '',
    expiryDate: '',
};
createSlice({ name: 'app', initialState, reducers: { symAndExpiry: (state, action) => { state.symbol = action.payload }, decrement: state => { state.value -= 1; } } });