import { createSlice } from "@reduxjs/toolkit";

const userSlice = createSlice({
     name: "user",

    initialState: {
        user: null
    },

    reducers: {
        login(state, action) {
            state.user = action.payload;
        },

        logout(state) {
            state.user = null;

        },

        editarPerfil(state, action) {
            state.user = {
                ...state.user,
                ...action.payload
            }


        }

        
    }

   
})

export default  userSlice.reducer;
export const {login, logout, editarPerfil} = userSlice.actions;

