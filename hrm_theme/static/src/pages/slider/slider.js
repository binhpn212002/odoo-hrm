/** @odoo-module **/
import { Component, useState, onWillUnmount, onWillStart} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class Slider extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            currentSlide: 0,
        });

        this.slides = [
            { url: "/hrm_theme/static/img/customer-relationship-management-crm-banner-vector-27056937.jpg", },
            { url: "/hrm_theme/static/img/isometric-crm-web-banner-customer-relationship-management-concept-business-internet-technology-vector-illustration_589019-4301.jpg" },
            { url: "/hrm_theme/static/img/crm-concept-banner-isometric-style-vector.jpg" },
        ];


        // Set up auto-slide with interval
        this.autoSlideInterval = setInterval(() => {
            this.nextSlide();
        }, 5000); // Auto-slide every 5 seconds
        onWillStart(async () => {
            const sliderImages = await this.rpc("/slider/images", {});
            // console.log(sliderImages)
            if(sliderImages.length !=0)
                this.slides = sliderImages
        })
        // Clean up interval when component unmounts
        onWillUnmount(() => {
            clearInterval(this.autoSlideInterval);
        });
    }

    nextSlide() {
        this.state.currentSlide =
            (this.state.currentSlide + 1) % this.slides.length;
    }

    prevSlide() {
        this.state.currentSlide =
            (this.state.currentSlide - 1 + this.slides.length) % this.slides.length;
    }

    resetAutoSlide() {
        clearInterval(this.autoSlideInterval);
        this.autoSlideInterval = setInterval(() => {
            this.nextSlide();
        }, 5000);
    }
}

Slider.template = "hrm_theme.SliderTemplate";