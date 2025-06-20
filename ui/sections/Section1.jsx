import React from 'react'
import Link from 'next/link'
import { Roboto_Condensed } from 'next/font/google';
const robotoCondensed = Roboto_Condensed({
  subsets: ['latin'],
  weight: ['400', '700'], // optional weights
  display: 'swap',
});

const Section1 = () => {
  return (
   <>
     <section className={`h-[90vh] w-full  mt-15 flex justify-center items-center px-6 ${robotoCondensed.className}`}>
        <header className="flex flex-col items-center text-center gap-6 max-w-3xl text-black">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight leading-snug">
            Welcome to <span className="text-red-600">Stockify</span>, <br className="hidden md:block" />
            Your Personal AI Architecture
          </h1>
          <p className="text-base md:text-lg mt-6 text-gray-600 leading-relaxed">
            Don't rush — our intelligent system helps you analyze market trends, <br />
            optimize investment strategies, and make informed decisions — tailored for you.<br />
            Let <span className="font-semibold text-black">Stockify</span> simplify the stock market, one insight at a time.
          </p>
          <Link href="/search">
          <button className="mt-4 px-6 py-2 bg-red-500 hover:bg-red-600 transition duration-300 ease-in-out rounded-full text-white text-base md:text-lg font-semibold shadow-lg hover:scale-105">
            🚀 Get Started
          </button>
          </Link>
        </header>
      </section>
   </>
  )
}

export default Section1
