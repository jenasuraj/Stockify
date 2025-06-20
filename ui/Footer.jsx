import React from 'react'

const Footer = () => {
  return (
    <>
    <footer className="w-full h-[20vh] bg-black text-white py-8 px-6 mt-12">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
        <p className="text-sm">&copy; {new Date().getFullYear()} Stockify.ai. All rights reserved.</p>

        <nav className="mt-4 md:mt-0  space-x-6">
          <a href="/about" className="hover:underline text-sm">
            About
          </a>
          <a href="/services" className="hover:underline text-sm">
            Services
          </a>
          <a href="/contact" className="hover:underline text-sm">
            Contact
          </a>
          <a href="/privacy" className="hover:underline text-sm">
            Privacy Policy
          </a>
        </nav>
      </div>
    </footer>
    </>
  )
}

export default Footer
