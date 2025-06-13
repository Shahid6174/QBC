import React from 'react';

// 🧠 Dynamically get current year
const currentYear = new Date().getFullYear();

const Footer = () => {
  return (
    <footer className="bg-light text-center text-lg-start mt-5 border-top shadow-sm">
      <div className="container py-3 d-flex flex-column flex-md-row justify-content-between align-items-center">
        
        {/* 📄 Copyright */}
        <span className="text-muted mb-2 mb-md-0">
          © {currentYear} Admin Panel. All rights reserved.
        </span>

        {/* 🧩 Future extension placeholder – Add links or credits */}
        <div className="footer-links">
          {/* Example: <a href="/privacy" className="text-muted me-3">Privacy</a> */}
        </div>
      </div>
    </footer>
  );
};

export default Footer;
