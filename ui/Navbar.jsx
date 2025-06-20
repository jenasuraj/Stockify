import React from 'react';
import { IoLogoFirefox } from 'react-icons/io5';
import Link from 'next/link';

const Navbar = () => {
  return (
    <header className="w-full h-[10vh] z-50 fixed">
      <nav className="max-w-7xl bg-white mx-auto h-full px-6 flex items-center justify-between">
        {/* Logo Section */}
       <Link href="/">
        <div className="flex items-center gap-2 text-red-600 font-bold text-2xl">
          <IoLogoFirefox size={40} />
          <span>Stockify</span>
        </div>
       </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex gap-8 text-gray-700 font-medium">
          <a href="#" className="hover:text-red-600 transition">Home</a>
          <a href="#" className="hover:text-red-600 transition">Dashboard</a>
          <a href="#" className="hover:text-red-600 transition">Markets</a>
          <a href="#" className="hover:text-red-600 transition">Contact</a>
        </div>

        {/* Action Button */}
        <div className="flex items-center gap-4">
          <button className="px-4 py-2 border border-green-500 text-green-500 rounded hover:bg-green-500 hover:text-white transition">
            Login
          </button>
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
