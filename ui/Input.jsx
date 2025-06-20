
"use client";

import React, { useState } from "react";
import axios from "axios";
import { Roboto_Condensed } from 'next/font/google';
const robotoCondensed = Roboto_Condensed({
  subsets: ['latin'],
  weight: ['400', '700'], // optional weights
  display: 'swap',
});


const Input = () => {
const [userData, setUserData] = useState({company:'',type:'',exchange:''});


  const invokeFastapi = async () => {
    try {
      console.log("the data is going ",userData.company , userData.type,userData.exchange)
      const response = await axios.post('http://127.0.0.1:8000/', {
        companyname: userData.company.toUpperCase(),companytype:userData.type,companyexchange:userData.exchange
      });
      if (response.data) {
        console.log("FastAPI says:", response.data.message);
      } else {
        console.log("No data returned from FastAPI");
      }
    } catch (error) {
      console.log("Error while sending data to FastAPI:", error.message);
    }
  };


const handleChange =(e)=>{
  const {name,value} = e.target
  setUserData( (prev)=>({...prev,[name]:value}))
} 

  return (
    <>
    <section className={`w-full h-screen flex justify-center  items-center flex-col ${robotoCondensed.className}`}>
       <div className="w-full h-auto gap-10 flex justify-center items-center">
         <form onSubmit={invokeFastapi} className="flex gap-10">
          <div className="flex flex-col text-lg gap-3">
          <label>Stock Name:</label>
          <input type="text" name="company" value={userData.company} onChange={handleChange} placeholder="Enter the stock name" className="bg-gray-100 border-none px-16 py-4 "/>
         </div>

         <div className="flex flex-col text-lg gap-3">
         <label>Research Type:</label>
         <select name="type" value={userData.type} onChange={handleChange} className="bg-gray-100 border-none px-16 py-4 " >
         <option value="Normal research">Normal Research</option>
         <option value="Deep research">Deep Research</option>
         </select>
         </div>

          <div className="flex flex-col text-lg gap-3">
         <label>Stock Exchange:</label>
         <select name="exchange" value={userData.exchange} onChange={handleChange} className="bg-gray-100 border-none px-16 py-4 " >
         <option value="NSE">NSE</option>
         <option value="BSE">BSE</option>
         </select>
         </div>

         <button className="px-8 py-4 border hover:border-red-600 mt-10 hover:text-red-600 bg-red-600 hover:cursor-pointer hover:bg-white text-white" type="submit">Start Research</button>
         </form>
       </div>
    </section>
    </>
  );
};

export default Input;


