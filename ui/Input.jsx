"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useRouter, useSearchParams } from "next/navigation";
import Lottie from "lottie-react";
import loadingAnim from "@/assets/loading.json";

const Input = () => {
  const [userData, setUserData] = useState({
    company: "",
    type: "",
    exchange: "",
  });
  const [apiResponse, setApiResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const invokeFastapi = async (e) => {
    e.preventDefault();
    if (!userData.company || !userData.exchange || !userData.type) return;

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/", {
        companyname: userData.company.toUpperCase(),
        companytype: userData.type,
        companyexchange: userData.exchange,
      });

      setUserData({ company: "", type: "", exchange: "" });

      if (response.data) {
        setApiResponse(response.data.message);
      } else {
        console.log("No data returned from FastAPI");
      }
    } catch (error) {
      console.error("Error while sending data to FastAPI:", error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserData((prev) => ({ ...prev, [name]: value }));
  };

  const send = () => {
    if (!apiResponse) return;
    router.push(`/search/slug/?data=${encodeURIComponent(apiResponse)}`);
  };

  return (
    <section className="relative w-full min-h-screen flex justify-center items-center px-4 py-12 bg-gray-50">
      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-white z-50 flex items-center justify-center">
          <Lottie animationData={loadingAnim} style={{ height: 500, width: 500 }} />
        </div>
      )}

      {/* Main Form */}
      {!loading && (
        <form
          onSubmit={invokeFastapi}
          className="w-full max-w-4xl bg-white shadow-xl rounded-2xl p-10 flex flex-col gap-6"
        >
          {/* Stock Name */}
          <div className="flex flex-col gap-2">
            <label htmlFor="company" className="text-lg font-semibold text-gray-700">
              Stock Name
            </label>
            <input
              type="text"
              id="company"
              name="company"
              value={userData.company}
              onChange={handleChange}
              placeholder="Enter the stock name"
              className="bg-gray-100 px-4 py-3 rounded-md outline-none focus:ring-2 focus:ring-red-400"
            />
          </div>

          {/* Research Type */}
          <div className="flex flex-col gap-2">
            <label htmlFor="type" className="text-lg font-semibold text-gray-700">
              Research Type
            </label>
            <select
              id="type"
              name="type"
              value={userData.type}
              onChange={handleChange}
              className="bg-gray-100 px-4 py-3 rounded-md outline-none focus:ring-2 focus:ring-red-400"
            >
              <option value="" disabled>
                Select research type
              </option>
              <option value="Normal research">Normal Research</option>
              <option value="Deep research">Deep Research</option>
            </select>
          </div>

          {/* Stock Exchange */}
          <div className="flex flex-col gap-2">
            <label htmlFor="exchange" className="text-lg font-semibold text-gray-700">
              Stock Exchange
            </label>
            <select
              id="exchange"
              name="exchange"
              value={userData.exchange}
              onChange={handleChange}
              className="bg-gray-100 px-4 py-3 rounded-md outline-none focus:ring-2 focus:ring-red-400"
            >
              <option value="" disabled>
                Select stock exchange
              </option>
              <option value="NSE">NSE</option>
              <option value="BSE">BSE</option>
            </select>
          </div>

          {/* Button Group */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-4">
            <button
              type="submit"
              className="px-6 py-3 rounded-md bg-red-600 text-white font-semibold hover:bg-white hover:text-red-600 hover:border hover:border-red-600 transition duration-300"
            >
              🚀 Start Research
            </button>

            {apiResponse && (
              <button
                type="button"
                onClick={send}
                className="px-6 py-3 rounded-md bg-blue-600 text-white font-semibold hover:bg-white hover:text-blue-600 hover:border hover:border-blue-600 transition duration-300"
              >
                📊 See Data
              </button>
            )}
          </div>
        </form>
      )}
    </section>
  );
};

export default Input;
