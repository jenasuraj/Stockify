"use client"
import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import Lottie from "lottie-react";
import up from "@/assets/up.json"
import down from "@/assets/down.json"
import stable from "@/assets/stable.json"
import error from "@/assets/error.json"

const page = () => {
  const searchParams = useSearchParams();
  const dataString = searchParams.get("data");
  const data = JSON.parse(dataString);
  const pe_ratio = parseInt(data.technical_data.PE_RATIO)
  const roe = parseFloat(data.technical_data.ROE)
  const eps = parseInt(data.technical_data.EPS)
  const mc = parseInt(data.technical_data.MARKET_CAPITAL)
  const conclusion = data.conclusion

  return (
    <section className="w-full min-h-screen bg-[#f9fafb] flex flex-col md:flex-row text-gray-800">
      
      {/* Left Panel */}
      <div className="w-full md:w-2/3 min-h-screen flex flex-col items-center justify-center gap-12 p-8">

        {/* Top Row */}
        <div className="flex flex-col md:flex-row w-full gap-8">
          {/* PE Ratio Box */}
          <div className="bg-white rounded-3xl shadow-md w-full p-6 flex flex-col items-center">
            {pe_ratio < 15 ? <Lottie animationData={up} style={{ height: 150 }} />
              : pe_ratio > 15 && pe_ratio < 30 ? <Lottie animationData={stable} style={{ height: 150 }} />
              : pe_ratio > 30 ? <Lottie animationData={down} style={{ height: 150 }} />
              : <Lottie animationData={error} loop />}
            <p className={`mt-4 text-lg font-semibold px-5 py-2 rounded-full 
              ${pe_ratio < 15 ? 'bg-green-500 text-white' :
                pe_ratio > 15 && pe_ratio < 30 ? 'bg-blue-600 text-white' :
                  'bg-red-500 text-white'}`}>
              PE RATIO = {pe_ratio}
            </p>
          </div>

          {/* ROE Box */}
          <div className="bg-white rounded-3xl shadow-md w-full p-6 flex flex-col items-center">
            {roe > 0.15 ? <Lottie animationData={up} style={{ height: 150 }} />
              : roe > 0.08 && roe < 0.15 ? <Lottie animationData={stable} style={{ height: 150 }} />
              : roe < 0.08 ? <Lottie animationData={down} style={{ height: 150 }} />
              : <Lottie animationData={error} loop />}
            <p className={`mt-4 text-lg font-semibold px-5 py-2 rounded-full 
              ${roe > 0.15 ? 'bg-green-500 text-white' :
                roe > 0.08 && roe < 0.15 ? 'bg-blue-600 text-white' :
                  'bg-red-500 text-white'}`}>
              ROE = {roe}
            </p>
          </div>
        </div>

        {/* Bottom Row */}
        <div className="flex flex-col md:flex-row w-full gap-8">
          {/* EPS Box */}
          <div className="bg-white rounded-3xl shadow-md w-full p-6 flex flex-col items-center">
            {eps > 50 ? <Lottie animationData={up} style={{ height: 150 }} />
              : eps >= 10 && eps < 50 ? <Lottie animationData={stable} style={{ height: 150 }} />
              : eps < 10 ? <Lottie animationData={down} style={{ height: 150 }} />
              : <Lottie animationData={error} loop />}
            <p className={`mt-4 text-lg font-semibold px-5 py-2 rounded-full 
              ${eps > 50 ? 'bg-green-500 text-white' :
                eps >= 10 && eps < 50 ? 'bg-blue-600 text-white' :
                  'bg-red-500 text-white'}`}>
              EPS = {eps}
            </p>
          </div>

          {/* Market Cap Box */}
          <div className="bg-white rounded-3xl shadow-md w-full p-6 flex flex-col items-center">
            {mc > 2000000000000 ? <Lottie animationData={up} style={{ height: 150 }} />
              : mc >= 500000000000 ? <Lottie animationData={stable} style={{ height: 150 }} />
              : mc < 500000000000 ? <Lottie animationData={down} style={{ height: 150 }} />
              : <Lottie animationData={error} loop />}
            <p className={`mt-4 text-lg font-semibold px-5 py-2 rounded-full 
              ${mc > 2000000000000 ? 'bg-green-500 text-white' :
                mc >= 500000000000 ? 'bg-blue-600 text-white' :
                  'bg-red-500 text-white'}`}>
              MARKET CAPITAL = {mc}
            </p>
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-full md:w-1/3 mt-10 bg-white min-h-screen shadow-inner p-8 flex flex-col gap-6 items-start justify-center">
        {/* News Box */}
        <div className="w-full min-h-[200px] bg-gray-100 rounded-3xl p-6 shadow-sm border border-gray-300">
          <h3 className="text-xl font-bold mb-3 text-gray-700">News</h3>
          <p className="text-gray-600 leading-relaxed">{data.news.news_data}</p>
        </div>

        {/* Conclusion Box */}
        <div className="w-full min-h-[200px] bg-gray-100 rounded-3xl p-6 shadow-sm border border-gray-300">
          <h3 className="text-xl font-bold mb-3 text-gray-700">Conclusion</h3>
          <p className="text-gray-600 leading-relaxed">{data.conclusion}</p>
        </div>
      </div>
    </section>
  )
}

export default page;
