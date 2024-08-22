import Image  from "next/image";
import Logo from "../../public/assests/disko.png";


const navLinks = [
    {name: 'Home'},{name : 'About'}
];

export function Navbar() { 
return(
<nav className=" bg-body-tertiary justify-beween px-[20px] py[16py] lg:container lg:mx-auto lg:px-10">
  <div className="container-fluid flex items-center justify-between px-4 py-2">
    <div className="flex items-center space-x-3">
      <Image src={Logo} alt="Logo" width="45" height="40"/>
      <div className="flex gap-x-6">
          {navLinks.map((link, index) => (
            <a className="nav-link" href="/" key={index}>
              {link.name}
            </a>
          ))}  
    </div>

    </div>
   </div>     
</nav>
);
}