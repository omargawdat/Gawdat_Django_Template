from datetime import date


class EmailTemplate:
    @staticmethod
    def otp(otp_code: int, expires_at: date, username: str = "there!"):
        app_name = "dars"
        exp_str = expires_at.strftime("%b %d, %Y %H:%M")

        html = f"""
       <div style="font-size:14px; line-height:1.6; color:#f0f9ff; margin-top:8px;">
           Hi <span style="color:#ffd700; font-weight:700;">{username}</span>, we’re excited to have you at
           <b>{app_name}</b>. Please use the code below to verify your email and begin your journey.
       </div>

       <div style="margin-top:16px; text-align:center;">
           <span
               style="display:inline-block; background:#ffffff; border:2px solid #3b82f6; border-radius:14px; padding:14px 22px;">
               <span class="otp"
                   style="font-weight:800; font-size:28px; letter-spacing:8px; color:#1e3a8a;">{otp_code}</span>
           </span>
       </div>
       <div style="margin-top:12px; font-size:12px; color:#e0f2fe; text-align:center;">
           This code expires at <strong>{exp_str}</strong>.
       </div>

       """  # noqa RUF001

        return html

    @staticmethod
    def reset_password(otp):
        pass
