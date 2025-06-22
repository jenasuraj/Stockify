import React from 'react';
import searchImg from '@/assets/search.png';
import { BsGraphUp } from "react-icons/bs";
import Image from 'next/image';

const Section4 = () => {
  return (
    <section className="w-full px-4 py-12 flex flex-col items-center mt-10">
      {/* Badge */}
      <div className="flex items-center gap-2 text-red-600 bg-red-50 rounded-2xl px-3 py-1 mb-4 text-sm sm:text-base">
        <BsGraphUp size={20} />
        Features
      </div>

      {/* Heading */}
      <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-center text-gray-800">
        See the statistics within 3 steps
      </h2>

      {/* Image */}
      <div className="w-full max-w-4xl mt-6 px-4 sm:px-6">
        <Image
          className="w-full h-auto rounded-lg border border-gray-100"
          src={searchImg}
          alt="search-image"
          priority
        />
      </div>
    </section>
  );
};

export default Section4;
