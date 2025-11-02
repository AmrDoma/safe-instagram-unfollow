"""
Safe Instagram Unfollow Script
Unfollows users from the "not_following_back" CSV file
Includes rate limiting, safety checks, and progress saving
"""

import requests
import csv
import time
import random
import json
from pathlib import Path

class SafeUnfollower:
    def __init__(self, sessionid, csrftoken):
        self.session = requests.Session()
        
        # Set cookies
        self.session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        self.session.cookies.set('csrftoken', csrftoken, domain='.instagram.com')
        
        # Set headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-CSRFToken': csrftoken,
            'X-IG-App-ID': '936619743392459',
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        
        self.unfollowed_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        
    def unfollow_user(self, user_id, username):
        """
        Unfollow a single user
        """
        url = f"https://www.instagram.com/api/v1/friendships/destroy/{user_id}/"
        
        try:
            response = self.session.post(url)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    print(f"   ✅ Unfollowed: @{username}")
                    self.unfollowed_count += 1
                    return True
                else:
                    print(f"   ❌ Failed: @{username} - {data}")
                    self.failed_count += 1
                    return False
            else:
                print(f"   ❌ Failed: @{username} - HTTP {response.status_code}")
                if response.status_code == 429:
                    print(f"   ⚠️  RATE LIMITED! Taking a long break...")
                    return 'rate_limited'
                self.failed_count += 1
                return False
                
        except Exception as e:
            print(f"   ❌ Error: @{username} - {e}")
            self.failed_count += 1
            return False


def load_csv(filepath):
    """Load the not_following_back CSV file"""
    users = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append({
                'user_id': row['user_id'],
                'username': row['username'],
                'full_name': row.get('full_name', ''),
                'is_verified': row.get('is_verified', 'False') == 'True'
            })
    
    return users


def save_progress(unfollowed_users, filepath='unfollow_progress.json'):
    """Save progress to resume later"""
    with open(filepath, 'w') as f:
        json.dump(unfollowed_users, f, indent=2)


def load_progress(filepath='unfollow_progress.json'):
    """Load previous progress"""
    if Path(filepath).exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return []


def main():
    print("=" * 70)
    print("Safe Instagram Unfollow Script")
    print("=" * 70)
    print("\n⚠️  SAFETY FEATURES:")
    print("   • Rate limiting with random delays (15-30 seconds between unfollows)")
    print("   • Batch limits (max unfollows per session)")
    print("   • Progress saving (resume anytime)")
    print("   • Skip verified accounts option")
    print("   • Confirmation before each batch")
    print("\n⚠️  INSTAGRAM LIMITS:")
    print("   • ~200 unfollows per hour is generally safe")
    print("   • ~400-500 unfollows per day maximum")
    print("   • Going too fast = temporary action block")
    print("=" * 70)
    
    # Get cookies
    print("\n📝 Enter your Instagram cookies:")
    sessionid = input("sessionid: ").strip()
    csrftoken = input("csrftoken: ").strip()
    
    if not sessionid or not csrftoken:
        print("❌ Both cookies are required")
        return
    
    # Get CSV file
    print("\n📁 CSV File:")
    csv_path = input("Enter path to not_following_back CSV file: ").strip()
    
    if not Path(csv_path).exists():
        print("❌ File not found")
        return
    
    # Load users
    print("\n🔄 Loading users from CSV...")
    users = load_csv(csv_path)
    print(f"✅ Found {len(users)} users in the list")
    
    # Load progress
    already_unfollowed = load_progress()
    already_unfollowed_ids = {u['user_id'] for u in already_unfollowed}
    
    # Filter out already unfollowed
    users = [u for u in users if u['user_id'] not in already_unfollowed_ids]
    
    if already_unfollowed:
        print(f"📊 Already unfollowed {len(already_unfollowed)} users (resuming)")
    
    if not users:
        print("✅ All users already unfollowed!")
        return
    
    print(f"📊 {len(users)} users remaining to unfollow")
    
    # Configuration
    print("\n" + "=" * 70)
    print("⚙️  Configuration:")
    
    skip_verified = input("\nSkip verified accounts? (y/n): ").strip().lower() == 'y'
    
    if skip_verified:
        verified_count = sum(1 for u in users if u['is_verified'])
        print(f"   Will skip {verified_count} verified accounts")
        users = [u for u in users if not u['is_verified']]
    
    batch_size = int(input("\nHow many to unfollow this session? (recommended: 50-100): ").strip() or "50")
    
    min_delay = int(input("Minimum delay between unfollows (seconds, recommended: 15): ").strip() or "15")
    max_delay = int(input("Maximum delay between unfollows (seconds, recommended: 30): ").strip() or "30")
    
    # Limit to batch size
    users_to_unfollow = users[:batch_size]
    
    print("\n" + "=" * 70)
    print(f"📋 Ready to unfollow {len(users_to_unfollow)} users")
    print(f"⏱️  Estimated time: {len(users_to_unfollow) * (min_delay + max_delay) / 2 / 60:.1f} minutes")
    print("=" * 70)
    
    # Show preview
    print("\n📄 First 10 users to unfollow:")
    for i, user in enumerate(users_to_unfollow[:10], 1):
        verified = "✓" if user['is_verified'] else " "
        print(f"   {i}. @{user['username']} {verified} - {user['full_name']}")
    
    if len(users_to_unfollow) > 10:
        print(f"   ... and {len(users_to_unfollow) - 10} more")
    
    # Final confirmation
    print("\n" + "=" * 70)
    confirm = input("Type 'YES' to start unfollowing: ").strip()
    
    if confirm != 'YES':
        print("❌ Cancelled")
        return
    
    # Start unfollowing
    print("\n🚀 Starting unfollow process...")
    print("=" * 70)
    
    unfollower = SafeUnfollower(sessionid, csrftoken)
    
    for i, user in enumerate(users_to_unfollow, 1):
        print(f"\n[{i}/{len(users_to_unfollow)}] @{user['username']}")
        
        result = unfollower.unfollow_user(user['user_id'], user['username'])
        
        if result == True:
            # Success - save progress
            already_unfollowed.append(user)
            save_progress(already_unfollowed)
            
        elif result == 'rate_limited':
            print("\n⚠️  RATE LIMITED BY INSTAGRAM!")
            print("   Your account is being protected from action block.")
            print(f"   Successfully unfollowed: {unfollower.unfollowed_count}")
            print(f"   Failed: {unfollower.failed_count}")
            print("\n💡 Recommendations:")
            print("   1. Wait at least 1-2 hours before running again")
            print("   2. Use longer delays (30-60 seconds)")
            print("   3. Reduce batch size (20-30 users)")
            print("\n   Progress has been saved. Run script again later to continue.")
            save_progress(already_unfollowed)
            break
        
        # Random delay between unfollows (unless it's the last one)
        if i < len(users_to_unfollow):
            delay = random.randint(min_delay, max_delay)
            print(f"   ⏳ Waiting {delay} seconds...")
            time.sleep(delay)
            
            # Extra long break every 20 unfollows
            if i % 20 == 0:
                extra_break = random.randint(60, 120)
                print(f"\n   ☕ Taking a longer break ({extra_break}s) to stay safe...")
                time.sleep(extra_break)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Session Summary")
    print("=" * 70)
    print(f"✅ Successfully unfollowed: {unfollower.unfollowed_count}")
    print(f"❌ Failed: {unfollower.failed_count}")
    print(f"📊 Total unfollowed (all time): {len(already_unfollowed)}")
    print(f"📋 Remaining: {len(users) - len(users_to_unfollow)}")
    
    if len(users) > len(users_to_unfollow):
        print(f"\n💡 Run the script again to continue with the next batch")
    else:
        print(f"\n✅ All users have been processed!")
    
    print("\n💾 Progress saved to: unfollow_progress.json")
    print("=" * 70)


if __name__ == "__main__":
    main()
