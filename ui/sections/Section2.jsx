import React from 'react'
import { Roboto_Condensed } from 'next/font/google';
import { GiArtificialHive } from "react-icons/gi";
import { FiDatabase } from "react-icons/fi";
import { RiAppsLine } from "react-icons/ri";
import { BsGraphUp } from "react-icons/bs";

const robotoCondensed = Roboto_Condensed({
  subsets: ['latin'],
  weight: ['400', '700'], 
  display: 'swap',
})

const Section2 = () => {
  return (
    <section className='w-full px-4 py-8 flex flex-col items-center'>
      <div className='text-red-600 gap-2 flex bg-red-50 rounded-2xl px-2 mb-5'><BsGraphUp color='red' size={20}/>The new efficient standard</div>
      <header className={`${robotoCondensed.className} text-2xl sm:text-3xl md:text-4xl font-bold text-center`}>
        Spend Less Time on Collection, More Time on Decisions
      </header>

      <div className='mt-6 w-full flex flex-col sm:flex-row flex-wrap justify-center items-center gap-6'>
        {/* Card 1 */}
        <div className='w-full sm:w-60 h-52 border border-gray-200 rounded-2xl px-6 py-8 flex flex-col justify-center items-center gap-4 shadow-sm'>
          <GiArtificialHive size={50} color='gray'/>
          <p className='text-sm text-center'>Let us do the research for you!</p>
        </div>

        {/* Card 2 */}
        <div className='w-full sm:w-60 h-52 border border-gray-200 rounded-2xl px-6 py-8 flex flex-col justify-center items-center gap-4 shadow-sm'>
          <FiDatabase size={50} color='gray'/>
          <p className='text-sm text-center'>Access the latest trends and news!</p>
        </div>

        {/* Card 3 */}
        <div className='w-full sm:w-60 h-52 border border-gray-200 rounded-2xl px-6 py-8 flex flex-col justify-center items-center gap-4 shadow-sm'>
          <RiAppsLine size={50} color='gray'/>
          <p className='text-sm text-center'>Trust AI, let AI provide valid info</p>
        </div>
      </div>
    </section>
  )
}

export default Section2
