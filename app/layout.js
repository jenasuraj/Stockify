import "./globals.css";
import Navbar from "@/ui/Navbar";
import Footer from "@/ui/Footer";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar/>
       <main className="flex items-center flex-col">
         {children}
       </main>
       <Footer/>
      </body>
    </html>
  );
}
