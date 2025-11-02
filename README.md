# Safe Instagram Unfollow Tool

Safely unfollow Instagram users who don't follow you back. Built-in rate limiting and safety features to prevent account blocks.

## 🌟 Features

- ✅ **Safe**: Built-in rate limiting (15-30 second delays)
- ✅ **Smart**: Automatic breaks every 20 unfollows
- ✅ **Resumable**: Progress saving - continue anytime
- ✅ **Protected**: Detects and stops on rate limits
- ✅ **Configurable**: Control batch sizes and delays
- ✅ **Selective**: Option to skip verified accounts
- ✅ **Transparent**: Shows progress and confirmations

## ⚠️ Instagram Safety Limits

Instagram has strict limits to prevent spam:

- ✅ **~200 unfollows/hour** is generally safe
- ✅ **~400-500 unfollows/day** maximum recommended
- ❌ **Going too fast = temporary action block (24-48 hours)**

This tool respects these limits to keep your account safe!

## 📋 Requirements

```bash
pip install requests
```

## 🚀 Quick Start

### 1. Get Your Cookies

1. Open [instagram.com](https://instagram.com) (logged in)
2. Press **F12** → **Application** → **Cookies**
3. Copy these cookies:
   - **sessionid** (required)
   - **csrftoken** (required for unfollowing)

### 2. Prepare Your CSV

You need a CSV file with users to unfollow. Format:

```csv
username,user_id,full_name,is_verified
example_user,123456789,Example User,False
```

**Tip**: Use the [Instagram Follower Scraper](https://github.com/yourusername/instagram-follower-scraper) to generate this file automatically!

### 3. Run the Script

```bash
python safe_unfollow.py
```

### 4. Configure Settings

```
sessionid: [paste]
csrftoken: [paste]
CSV file path: downloads/username_not_following_back.csv

Skip verified accounts? y
How many to unfollow this session? 50
Min delay (seconds)? 15
Max delay (seconds)? 30
```

### 5. Confirm and Go!

Review the list, type `YES`, and let it run safely!

## 📊 Recommended Strategy

### For First-Time Users

**Day 1, Morning:**

- Unfollow 50-100 users
- Use 20-30 second delays

**Day 1, Afternoon (wait 3-4 hours):**

- Unfollow another 50-100 users

**Day 2 onwards:**

- Continue with 100-200 per day
- Spread throughout the day

### For Large Cleanup (1000+ unfollows)

- **Daily limit**: 200 unfollows
- **Sessions**: 2-3 per day
- **Delays**: 20-30 seconds minimum
- **Timeline**: ~5-10 days per 1000 unfollows

## 💾 Progress Saving

The script saves progress to `unfollow_progress.json` after each successful unfollow.

**Benefits:**

- ✅ Resume anytime if interrupted
- ✅ Survive crashes/errors
- ✅ Track what you've unfollowed
- ✅ Avoid duplicates

**Important:**

- ⚠️ Don't delete `unfollow_progress.json` while cleaning up
- ⚠️ Backup this file if needed

## 🛡️ Safety Features

### Rate Limit Detection

```
⚠️  RATE LIMITED BY INSTAGRAM!
   Your account is being protected from action block.
   Wait 1-2 hours before running again.
```

The script stops immediately if rate limited and saves progress.

### Automatic Breaks

- 15-30 second delays between each unfollow
- 60-120 second breaks every 20 unfollows
- Random delays to appear more human

### Verification Skip

Skip verified accounts automatically - they're usually:

- Celebrities
- Brands
- Public figures
- Less likely to follow back anyway

## 🔧 Advanced Configuration

### Custom Delays

Edit the script to change timing:

```python
min_delay = 20  # Minimum seconds between unfollows
max_delay = 40  # Maximum seconds between unfollows
batch_size = 30  # Users per session
```

### Resume After Rate Limit

If you get rate limited:

1. **Wait**: 2-3 hours minimum
2. **Increase delays**: 30-60 seconds
3. **Reduce batch**: 20-30 per session
4. **Run again**: Progress will resume automatically

## 📝 Example Session

```bash
$ python safe_unfollow.py

Safe Instagram Unfollow Script
==================================================

sessionid: abc123...xyz
csrftoken: def456...uvw
CSV file: downloads/user_not_following_back.csv

✅ Found 3,922 users in the list
📊 Already unfollowed 50 users (resuming)
📊 3,872 users remaining to unfollow

Skip verified accounts? y
   Will skip 45 verified accounts

How many to unfollow this session? 50
Min delay (seconds)? 20
Max delay (seconds)? 35

📋 Ready to unfollow 50 users
⏱️  Estimated time: 22.5 minutes

Type 'YES' to start: YES

🚀 Starting unfollow process...

[1/50] @user1
   ✅ Unfollowed: @user1
   ⏳ Waiting 27 seconds...

[2/50] @user2
   ✅ Unfollowed: @user2
   ⏳ Waiting 22 seconds...

...

[20/50] @user20
   ✅ Unfollowed: @user20
   ☕ Taking a longer break (95s) to stay safe...

...

📊 Session Summary
==================================================
✅ Successfully unfollowed: 50
❌ Failed: 0
📊 Total unfollowed (all time): 100
📋 Remaining: 3,822

💡 Run the script again to continue with the next batch
💾 Progress saved to: unfollow_progress.json
```

## ⚠️ Common Issues

### "HTTP 429" - Rate Limited

**Solution:**

- Wait 2-3 hours
- Increase delays (30-60 sec)
- Reduce batch size (20-30)
- Try again later

### Cookies Expired

**Solution:**

- Get fresh cookies from browser
- Make sure you're still logged in
- Don't log out while using the tool

### Instagram Asks for Verification

**Solution:**

- This is normal for unusual activity
- Verify via email/SMS
- Wait 24 hours
- Continue more slowly

## 🔒 Security & Privacy

### Your Cookies

- ⚠️ **Never share your sessionid/csrftoken**
- They provide full access to your account
- Treat them like your password

### Account Safety

- ✅ Works with 2FA (cookies bypass it)
- ✅ Works with private accounts
- ✅ Uses official Instagram API
- ❌ Cannot get your account banned (if used responsibly)

### What Instagram Sees

- Normal API calls (same as website)
- Similar to manual unfollowing
- Rate limiting makes it look human

## 🤝 Contributing

Issues? Improvements? Contributions welcome!

- Report bugs via Issues
- Submit PRs with improvements
- Share your experience
- Star if it helped you! ⭐

## ⚖️ Legal & Ethics

### Disclaimer

- Use at your own risk
- Respect Instagram's Terms of Service
- Don't abuse or harass users
- Follow rate limits
- Be ethical and responsible

### Not Responsible For

- Account blocks/bans from misuse
- Rate limiting violations
- Any damage from improper use

### Recommended Use

- Clean up your own account
- Remove inactive/bot accounts
- Manage your following list
- Stay within safe limits

## 📜 License

MIT License - Free to use, modify, and distribute.

## 🙏 Acknowledgments

- Instagram API reverse engineering community
- Users who requested safer unfollow tools
- Everyone practicing good social media hygiene

## 💡 Tips for Best Results

1. **Start slow**: First session = 20-30 unfollows only
2. **Be patient**: Spread over days, not hours
3. **Stay logged in**: Don't log out from browser
4. **Monitor**: Check Instagram app for any warnings
5. **Backup progress**: Save `unfollow_progress.json`
6. **Use during normal hours**: When you usually use Instagram

## ⭐ If This Helped You

- Star this repository
- Share with friends
- Report bugs/improvements
- Consider contributing

---

**Made with ❤️ for responsible Instagram users**

_Not affiliated with or endorsed by Instagram/Meta_

## 📞 Support

Having issues? Check:

1. [Troubleshooting](#-common-issues) section above
2. [Issues](https://github.com/yourusername/safe-instagram-unfollow/issues) page
3. Make sure you're using latest version

---

**Remember: Slow and steady wins the race! 🐢**
