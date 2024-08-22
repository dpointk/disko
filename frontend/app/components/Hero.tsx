import Image  from "next/image";
import k8s from "../../public/assests/k8s.svg"
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
                <div className="flex justify-center gap-4 mt-20">
                    <Link  className="bg-[#4328EB] w-1/2 max-w-xs text-4xl text-white rounded-md py-3 text-center" href="./statistics">
                        Image Statistics
                    </Link>
                    <Link className="bg-[#4328EB] w-1/2 max-w-xs text-4xl text-white rounded-md py-3 text-center" href="./images">
                        All The Images
                    </Link>
                    <button className="bg-[#4328EB] w-1/2 max-w-xs text-4xl text-white rounded-md py-3 text-center" >
                        Start Disko

                    </button>
                </div>
                <div className="flex justify-center mt-9">
                <Image src={k8s} alt="k8s" width="500" height="500" className="-ml-4 h-[30px] sm:h-[400px] lg:-mb-15 lg:h-auto xl:w-[15%]"/>
                </div>
            </div>
        </div>
    );
}