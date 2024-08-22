import Image  from "next/image";

import Logo from "../../public/assests/disko.png"

import Link from "next/link";


export function Hero(){
     return (
        <div className="pt-4">
            <div className="px-[20px]">
                <h1 className="text-center text-8xl leading-tight font-inter text-[#172026]">
                    Work with Disko
                </h1>
                <p className="text-center pt-3 text-3xl leading-relaxed max-w-2xl mx-auto mt-15">
                    Disko is an open source tool, designed to manage and
                    facilitate operations in disconnected (air-gapped)
                    environments. It has three main features: Statistics of
                    Images per Registry, Copy Images Between Registries,
                    and Migrate Images in Kubernetes.
                </p>
                <div className="flex justify-center">
                    <Image src={Logo} alt="Logo" width="200" height="200"/>
                </div>
                <div className="flex justify-center">
                    <Link  className="button-big" href="./statistics">
                        Start Disko
                    </Link>
                </div>
                <div className="flex justify-center mt-9">
                </div>
            </div>
        </div>
    );
}