
import React from 'react';
import stock_data from '@/assets/stock_data.png';
import Image from 'next/image';

const Section3 = () => {
  return (
    <section className="w-full px-4 py-12 flex flex-col items-center mt-10">
   

      {/* Heading */}
      <h2 className="text-2xl sm:text-3xl md:text-4xl mb-5 font-bold text-center text-gray-800">
        Get familier with the pillars of the company 
      </h2>
      <p>Not only 1 or 2 , get all the basic pillar data from stockify's ai such as pe ratio, pes, roe and market capital and also get a complete overview about company</p>

      {/* Image */}
      <div className="w-full max-w-4xl mt-6 px-4 sm:px-6">
        <Image
          className="w-full h-auto rounded-lg border border-gray-300"
          src={stock_data}
          alt="search-image"
          priority
        />
      </div>
    </section>
  );
};

export default Section3;
