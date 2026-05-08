import random
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Trip, Itinerary, UserProfile, Hotel, SavedTrip, RecentPlace, Payment, Destination
from .forms import UserRegistrationForm, UserProfileForm, TripPlannerForm, PaymentForm, INDIAN_STATES
from django.db.models import Q
from django.http import JsonResponse

# --- AI Logic Simulation ---
class DiscoveryAI:
    HUBS = {
        'delhi': [
            {
                'name': 'Humayun\'s Tomb',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1587135941948-670b381f08ce',
                'description': 'A magnificent precursor to the Taj Mahal, this UNESCO site is the first garden-tomb on the Indian subcontinent.',
                'distance': '5 km from Center',
                'best_time': 'October to March',
                'entry_fee': '₹40 (Indians)',
                'famous_food': 'Nizamuddin Kebabs',
                'suitability': ['Family', 'Couples'],
                'photo_spots': 'The central arch.',
                'route': 'Metro Line 6.',
                'safety_tips': 'Stay on paths.',
                'budget': '₹500 - ₹1000',
                'hotels': [
                    {'name': 'ITC Maurya', 'price': '₹15,000', 'rating': '4.9'},
                    {'name': 'The Oberoi', 'price': '₹18,000', 'rating': '5.0'}
                ],
                'transport': {
                    'flights': [{'time': '06:30 AM', 'cost': '₹4,200'}, {'time': '04:15 PM', 'cost': '₹5,500'}],
                    'trains': [{'time': '08:00 AM', 'cost': '₹1,800'}, {'time': '10:30 PM', 'cost': '₹2,400'}],
                    'buses': [{'time': '07:00 AM', 'cost': '₹900'}, {'time': '11:00 PM', 'cost': '₹1,200'}]
                },
                'nearby_attractions': [
                    {'name': 'India Gate', 'image': 'https://images.unsplash.com/photo-1585123334904-845d60e97b29'},
                    {'name': 'Red Fort', 'image': 'https://images.unsplash.com/photo-1598305312884-219195a63967'}
                ]
            },
            {
                'name': 'Lotus Temple',
                'category': 'Temples',
                'image': 'https://images.unsplash.com/photo-1564507592333-c60657eea523',
                'description': 'A Baháʼí House of Worship notable for its flowerlike shape.',
                'distance': '10 km from Center',
                'best_time': 'Evening',
                'entry_fee': 'Free',
                'famous_food': 'Kalkaji street food',
                'suitability': ['Solo', 'Family'],
                'photo_spots': 'The surrounding pools.',
                'route': 'Violet Line Metro.',
                'safety_tips': 'Silence inside.',
                'budget': '₹100 - ₹300',
                'hotels': [
                    {'name': 'Eros Hotel', 'price': '₹8,000', 'rating': '4.5'},
                    {'name': 'Bloomrooms', 'price': '₹3,500', 'rating': '4.2'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '₹3,500'}, {'time': '07:30 PM', 'cost': '₹4,800'}],
                    'trains': [{'time': '06:00 AM', 'cost': '₹800'}, {'time': '09:00 PM', 'cost': '₹1,200'}],
                    'buses': [{'time': '05:00 AM', 'cost': '₹400'}, {'time': '10:00 PM', 'cost': '₹600'}]
                },
                'nearby_attractions': [
                    {'name': 'Iskcon Temple', 'image': 'https://images.unsplash.com/photo-1604537466158-719b1972edd8'},
                    {'name': 'Nehru Planetarium', 'image': 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa'}
                ]
            }
        ],
        'mumbai': [
            {
                'name': 'Gateway of India',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1566550970639-5d98bc19ef84',
                'description': 'An arch-monument built during the 20th century in Bombay.',
                'distance': '0 km from Center',
                'best_time': 'Morning/Evening',
                'entry_fee': 'Free',
                'famous_food': 'Vada Pav at Colaba',
                'suitability': ['Friends', 'Family'],
                'photo_spots': 'The arch with the Taj Hotel.',
                'route': 'Local train to CST.',
                'safety_tips': 'Watch for crowds.',
                'budget': '₹200 - ₹500',
                'hotels': [
                    {'name': 'The Taj Mahal Palace', 'price': '₹25,000', 'rating': '5.0'},
                    {'name': 'Hotel Marine Plaza', 'price': '₹10,000', 'rating': '4.4'}
                ],
                'transport': {
                    'flights': [{'time': '07:45 AM', 'cost': '₹5,600'}, {'time': '05:30 PM', 'cost': '₹6,200'}],
                    'trains': [{'time': '06:15 AM', 'cost': '₹2,100'}, {'time': '09:45 PM', 'cost': '₹2,800'}],
                    'buses': [{'time': '08:00 AM', 'cost': '₹1,100'}, {'time': '10:00 PM', 'cost': '₹1,500'}]
                }
            }
        ],
        'kerala': [
            {
                'name': 'Alleppey Backwaters',
                'category': 'Nature',
                'image': 'https://images.unsplash.com/photo-1593693397690-362cb9666fc2',
                'description': 'Famous for its houseboat cruises that pass through serene canals and lagoons.',
                'distance': '2 km from Alleppey Town',
                'best_time': 'September to March',
                'entry_fee': 'Houseboat rentals vary',
                'famous_food': 'Karimeen Pollichathu',
                'suitability': ['Couples', 'Family'],
                'photo_spots': 'Sunset from a houseboat.',
                'route': 'Kochi Airport -> Cab.',
                'safety_tips': 'Check houseboat license.',
                'budget': '₹5000 - ₹15000',
                'hotels': [
                    {'name': 'Vasundhara Sarovar', 'price': '₹12,000', 'rating': '4.8'},
                    {'name': 'Lemon Tree Vembanad', 'price': '₹7,000', 'rating': '4.3'}
                ],
                'transport': {
                    'flights': [{'time': '08:20 AM', 'cost': '₹6,500'}, {'time': '03:40 PM', 'cost': '₹7,200'}],
                    'trains': [{'time': '07:00 AM', 'cost': '₹2,400'}, {'time': '11:15 PM', 'cost': '₹3,100'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹1,200'}, {'time': '09:00 PM', 'cost': '₹1,800'}]
                }
            }
        ],
        'goa': [
            {
                'name': 'Baga Beach',
                'category': 'Adventure',
                'image': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2',
                'description': 'The most famous beach in Goa, known for water sports and vibrant nightlife.',
                'distance': '15 km from Panjim',
                'best_time': 'November to February',
                'entry_fee': 'Free',
                'famous_food': 'Bebinca, Prawn Balchao',
                'suitability': ['Friends', 'Couples'],
                'photo_spots': 'Near Tito\'s Lane.',
                'route': 'Rent a scooty.',
                'safety_tips': 'Swim in designated zones.',
                'budget': '₹2000 - ₹8000',
                'hotels': [
                    {'name': 'Resort Rio', 'price': '₹9,000', 'rating': '4.6'},
                    {'name': 'Hard Rock Hotel', 'price': '₹11,000', 'rating': '4.7'}
                ],
                'transport': {
                    'flights': [{'time': '10:15 AM', 'cost': '₹4,800'}, {'time': '08:45 PM', 'cost': '₹5,900'}],
                    'trains': [{'time': '09:30 AM', 'cost': '₹1,900'}, {'time': '11:50 PM', 'cost': '₹2,500'}],
                    'buses': [{'time': '07:15 AM', 'cost': '₹850'}, {'time': '10:45 PM', 'cost': '₹1,300'}]
                }
            }
        ],
        'rajasthan': [
            {
                'name': 'Hawa Mahal',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1599661046289-e31897846e41',
                'description': 'The "Palace of Winds", a stunning five-story exterior resembling a honeycomb.',
                'distance': '0 km from Center',
                'best_time': 'Early Morning',
                'entry_fee': '₹50',
                'famous_food': 'Rawat Piaz Kachori',
                'suitability': ['Family', 'History buffs'],
                'photo_spots': 'From Wind View Cafe.',
                'route': 'Auto rickshaw.',
                'safety_tips': 'Beware of touts.',
                'budget': '₹300 - ₹700',
                'hotels': [
                    {'name': 'Rambagh Palace', 'price': '₹45,000', 'rating': '5.0'},
                    {'name': 'Jai Mahal Palace', 'price': '₹20,000', 'rating': '4.8'}
                ],
                'transport': {
                    'flights': [{'time': '09:50 AM', 'cost': '₹3,200'}, {'time': '06:25 PM', 'cost': '₹4,100'}],
                    'trains': [{'time': '08:15 AM', 'cost': '₹1,400'}, {'time': '10:40 PM', 'cost': '₹1,900'}],
                    'buses': [{'time': '06:45 AM', 'cost': '₹700'}, {'time': '11:30 PM', 'cost': '₹1,100'}]
                }
            }
        ],
        'himachal': [
            {
                'name': 'Rohtang Pass',
                'category': 'Adventure',
                'image': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23',
                'description': 'A high mountain pass connecting Kullu Valley with Lahaul and Spiti.',
                'distance': '51 km from Manali',
                'best_time': 'May to October',
                'entry_fee': 'Permit required (₹550)',
                'famous_food': 'Siddu with ghee',
                'suitability': ['Friends', 'Adventure'],
                'photo_spots': 'Beas Kund view.',
                'route': 'HRTC or Private Taxi.',
                'safety_tips': 'Carry warm clothes.',
                'budget': '₹2000 - ₹5000',
                'hotels': [
                    {'name': 'Span Resort & Spa', 'price': '₹15,000', 'rating': '4.7'},
                    {'name': 'The Himalayan', 'price': '₹12,000', 'rating': '4.6'}
                ],
                'transport': {
                    'flights': [{'time': '11:00 AM', 'cost': '₹7,500'}, {'time': '02:00 PM', 'cost': '₹8,800'}],
                    'trains': [{'time': '05:30 AM', 'cost': '₹2,800'}, {'time': '09:20 PM', 'cost': '₹3,500'}],
                    'buses': [{'time': '07:30 AM', 'cost': '₹1,500'}, {'time': '10:15 PM', 'cost': '₹2,200'}]
                }
            }
        ],
        'tamil nadu': [
            {
                'name': 'Meenakshi Temple',
                'category': 'Temples',
                'image': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220',
                'description': 'A historic Hindu temple located on the southern bank of the Vaigai River.',
                'distance': '1 km from Madurai Center',
                'best_time': 'April (Chithirai Festival)',
                'entry_fee': 'Free',
                'famous_food': 'Jigarthanda',
                'suitability': ['Family', 'Spiritual'],
                'photo_spots': 'Gopurams from outside.',
                'route': 'Madurai Railway Station.',
                'safety_tips': 'Dress modestly.',
                'budget': '₹200 - ₹600',
                'hotels': [
                    {'name': 'Heritage Madurai', 'price': '₹8,000', 'rating': '4.5'},
                    {'name': 'Gateway Hotel', 'price': '₹10,000', 'rating': '4.4'}
                ],
                'transport': {
                    'flights': [{'time': '08:00 AM', 'cost': '₹5,200'}, {'time': '04:30 PM', 'cost': '₹6,100'}],
                    'trains': [{'time': '07:15 AM', 'cost': '₹1,900'}, {'time': '11:45 PM', 'cost': '₹2,600'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹950'}, {'time': '10:30 PM', 'cost': '₹1,400'}]
                }
            }
        ],
        'tokyo': [
            {
                'name': 'Shibuya Crossing',
                'category': 'Adventure',
                'image': 'https://images.unsplash.com/photo-1542051841857-5f90071e7989',
                'description': 'The world\'s busiest pedestrian crossing, a must-see for urban explorers.',
                'distance': '0 km from Shibuya Station',
                'best_time': 'Night',
                'entry_fee': 'Free',
                'famous_food': 'Ichiran Ramen',
                'suitability': ['Solo', 'Friends'],
                'photo_spots': 'Starbucks window view.',
                'route': 'JR Yamanote Line.',
                'safety_tips': 'Follow traffic lights.',
                'budget': '¥1000 - ¥3000',
                'hotels': [
                    {'name': 'Park Hyatt Tokyo', 'price': '¥80,000', 'rating': '4.9'},
                    {'name': 'Shibuya Stream Excel', 'price': '¥30,000', 'rating': '4.5'}
                ],
                'transport': {
                    'flights': [{'time': '10:00 AM', 'cost': '¥50,000'}, {'time': '06:00 PM', 'cost': '¥65,000'}],
                    'trains': [{'time': '07:00 AM', 'cost': '¥15,000'}, {'time': '09:00 PM', 'cost': '¥15,000'}],
                    'buses': [{'time': '08:00 AM', 'cost': '¥3,000'}, {'time': '10:00 PM', 'cost': '¥3,000'}]
                }
            }
        ],
        'london': [
            {
                'name': 'Tower Bridge',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad',
                'description': 'A combined bascule and suspension bridge in London.',
                'distance': '2 km from Center',
                'best_time': 'Sunset',
                'entry_fee': 'Free (walking across)',
                'famous_food': 'Fish and Chips at Borough Market',
                'suitability': ['Couples', 'Family'],
                'photo_spots': 'From the North Bank.',
                'route': 'London Bridge Tube Station.',
                'safety_tips': 'Mind the gap.',
                'budget': '£10 - £30',
                'hotels': [
                    {'name': 'The Savoy', 'price': '£600', 'rating': '5.0'},
                    {'name': 'Shangri-La at The Shard', 'price': '£700', 'rating': '4.9'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '£400'}, {'time': '05:00 PM', 'cost': '£550'}],
                    'trains': [{'time': '08:00 AM', 'cost': '£80'}, {'time': '10:00 PM', 'cost': '£80'}],
                    'buses': [{'time': '07:30 AM', 'cost': '£20'}, {'time': '11:30 PM', 'cost': '£20'}]
                },
                'nearby_attractions': [
                    {'name': 'London Eye', 'image': 'https://images.unsplash.com/photo-1505761671935-60b3a7427bad'},
                    {'name': 'Big Ben', 'image': 'https://images.unsplash.com/photo-1529655683826-aba9b3e77383'}
                ]
            }
        ],
        'france': [
            {
                'name': 'Eiffel Tower',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34',
                'description': 'The iconic iron lattice tower on the Champ de Mars in Paris.',
                'distance': '0 km from Paris Center',
                'best_time': 'Sunset',
                'entry_fee': '€25',
                'famous_food': 'Croissants, Macarons',
                'suitability': ['Couples', 'Family'],
                'photo_spots': 'Trocadero Gardens.',
                'route': 'Metro Line 6/9.',
                'safety_tips': 'Beware of street scammers.',
                'budget': '€50 - €150',
                'hotels': [
                    {'name': 'Shangri-La Paris', 'price': '€1,200', 'rating': '5.0'},
                    {'name': 'Hotel Pullman', 'price': '€450', 'rating': '4.6'}
                ],
                'transport': {
                    'flights': [{'time': '10:00 AM', 'cost': '€350'}, {'time': '08:00 PM', 'cost': '€420'}],
                    'trains': [{'time': '07:00 AM', 'cost': '€60'}, {'time': '09:00 PM', 'cost': '€60'}],
                    'buses': [{'time': '08:00 AM', 'cost': '€15'}, {'time': '11:00 PM', 'cost': '€15'}]
                },
                'nearby_attractions': [
                    {'name': 'Louvre Museum', 'image': 'https://images.unsplash.com/photo-1543349689-9a4d426bee8e'},
                    {'name': 'Arc de Triomphe', 'image': 'https://images.unsplash.com/photo-1509439581779-6298f75bf6e5'}
                ]
            }
        ],
        'italy': [
            {
                'name': 'Colosseum',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5',
                'description': 'The largest ancient amphitheatre ever built, located in Rome.',
                'distance': '0 km from Rome Center',
                'best_time': 'Morning',
                'entry_fee': '€16',
                'famous_food': 'Gelato, Carbonara',
                'suitability': ['History buffs', 'Family'],
                'photo_spots': 'From Via Nicola Salvi.',
                'route': 'Metro Line B.',
                'safety_tips': 'Book tickets in advance.',
                'budget': '€40 - €120',
                'hotels': [
                    {'name': 'Hotel Hassler', 'price': '€900', 'rating': '4.9'},
                    {'name': 'Hotel Artemide', 'price': '€350', 'rating': '4.7'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '€280'}, {'time': '07:00 PM', 'cost': '€350'}],
                    'trains': [{'time': '08:00 AM', 'cost': '€50'}, {'time': '10:00 PM', 'cost': '€50'}],
                    'buses': [{'time': '07:00 AM', 'cost': '€10'}, {'time': '11:00 PM', 'cost': '€10'}]
                },
                'nearby_attractions': [
                    {'name': 'Trevi Fountain', 'image': 'https://images.unsplash.com/photo-1525874684015-58379d421a52'},
                    {'name': 'Vatican Museums', 'image': 'https://images.unsplash.com/photo-1549466600-02cf417bb742'}
                ]
            }
        ],
        'usa': [
            {
                'name': 'Times Square',
                'category': 'Adventure',
                'image': 'https://images.unsplash.com/photo-1534430480872-3498386e7a0c',
                'description': 'The neon-lit junction of Broadway and Seventh Avenue in New York City.',
                'distance': '0 km from Midtown NYC',
                'best_time': 'Night',
                'entry_fee': 'Free',
                'famous_food': 'NYC Pizza, Hot Dogs',
                'suitability': ['Solo', 'Friends'],
                'photo_spots': 'Red stairs in center.',
                'route': 'N, Q, R Subway lines.',
                'safety_tips': 'Stay aware of crowds.',
                'budget': '$50 - $200',
                'hotels': [
                    {'name': 'Marriott Marquis', 'price': '$550', 'rating': '4.5'},
                    {'name': 'The Knickerbocker', 'price': '$650', 'rating': '4.7'}
                ],
                'transport': {
                    'flights': [{'time': '08:00 AM', 'cost': '$450'}, {'time': '10:00 PM', 'cost': '$450'}],
                    'trains': [{'time': '07:00 AM', 'cost': '$90'}, {'time': '09:00 PM', 'cost': '$90'}],
                    'buses': [{'time': '06:00 AM', 'cost': '$30'}, {'time': '11:00 PM', 'cost': '$30'}]
                },
                'nearby_attractions': [
                    {'name': 'Central Park', 'image': 'https://images.unsplash.com/photo-1526333699558-89bf1658467b'},
                    {'name': 'Statue of Liberty', 'image': 'https://images.unsplash.com/photo-1605130284535-11dd9eedc58a'}
                ]
            }
        ],
        'canada': [
            {
                'name': 'Niagara Falls',
                'category': 'Nature',
                'image': 'https://images.unsplash.com/photo-1533094602577-198d3beba81d',
                'description': 'A group of three waterfalls at the southern end of Niagara Gorge, spanning the border between Ontario and New York.',
                'distance': '130 km from Toronto',
                'best_time': 'June to August',
                'entry_fee': 'Free (Park)',
                'famous_food': 'Poutine, Beavertails',
                'suitability': ['Family', 'Couples'],
                'photo_spots': 'Journey Behind the Falls.',
                'route': 'GO Train from Toronto.',
                'safety_tips': 'Stay behind railings.',
                'budget': 'CAD 50 - CAD 150',
                'hotels': [
                    {'name': 'Sheraton Fallsview', 'price': 'CAD 400', 'rating': '4.8'},
                    {'name': 'Hilton Niagara Falls', 'price': 'CAD 350', 'rating': '4.7'}
                ],
                'transport': {
                    'flights': [{'time': '08:00 AM', 'cost': 'CAD 120'}, {'time': '06:00 PM', 'cost': 'CAD 150'}],
                    'trains': [{'time': '07:30 AM', 'cost': 'CAD 25'}, {'time': '09:30 PM', 'cost': 'CAD 25'}],
                    'buses': [{'time': '06:00 AM', 'cost': 'CAD 15'}, {'time': '11:00 PM', 'cost': 'CAD 15'}]
                },
                'nearby_attractions': [
                    {'name': 'Skylon Tower', 'image': 'https://images.unsplash.com/photo-1510113333310-911802996d91'},
                    {'name': 'Clifton Hill', 'image': 'https://images.unsplash.com/photo-1542385151-efd9000785a0'}
                ]
            }
        ],
        'switzerland': [
            {
                'name': 'Jungfraujoch',
                'category': 'Adventure',
                'image': 'https://images.unsplash.com/photo-1527668752968-14dc70a27c95',
                'description': 'Known as the "Top of Europe", a high-altitude railway station in the Bernese Alps.',
                'distance': '10 km from Interlaken',
                'best_time': 'Year-round',
                'entry_fee': 'CHF 200 (Train)',
                'famous_food': 'Cheese Fondue, Chocolate',
                'suitability': ['Adventure', 'Couples'],
                'photo_spots': 'Sphinx Observatory.',
                'route': 'Jungfrau Railway.',
                'safety_tips': 'Beware of altitude sickness.',
                'budget': 'CHF 100 - CHF 300',
                'hotels': [
                    {'name': 'Victoria-Jungfrau', 'price': 'CHF 700', 'rating': '4.9'},
                    {'name': 'Hotel Belvedere', 'price': 'CHF 400', 'rating': '4.6'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': 'CHF 300'}, {'time': '07:00 PM', 'cost': 'CHF 400'}],
                    'trains': [{'time': '08:00 AM', 'cost': 'CHF 80'}, {'time': '10:00 PM', 'cost': 'CHF 80'}],
                    'buses': [{'time': '07:00 AM', 'cost': 'CHF 20'}, {'time': '11:00 PM', 'cost': 'CHF 20'}]
                },
                'nearby_attractions': [
                    {'name': 'Lake Brienz', 'image': 'https://images.unsplash.com/photo-1511200057375-300405230c11'},
                    {'name': 'Lauterbrunnen Valley', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4'}
                ]
            }
        ],
        'japan': [
            {
                'name': 'Mount Fuji',
                'category': 'Nature',
                'image': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
                'description': 'Japan\'s highest mountain and an iconic symbol of the country.',
                'distance': '100 km from Tokyo',
                'best_time': 'July to September (Climbing)',
                'entry_fee': '¥1,000 (Donation)',
                'famous_food': 'Houtou Noodles',
                'suitability': ['Friends', 'Adventure'],
                'photo_spots': 'Chureito Pagoda.',
                'route': 'Bus from Shinjuku.',
                'safety_tips': 'Check weather forecasts.',
                'budget': '¥3000 - ¥8000',
                'hotels': [
                    {'name': 'Hoshinoya Fuji', 'price': '¥90,000', 'rating': '4.9'},
                    {'name': 'Konansou', 'price': '¥50,000', 'rating': '4.7'}
                ],
                'transport': {
                    'flights': [{'time': '08:00 AM', 'cost': '¥30,000'}, {'time': '06:00 PM', 'cost': '¥45,000'}],
                    'trains': [{'time': '07:30 AM', 'cost': '¥12,000'}, {'time': '09:30 PM', 'cost': '¥12,000'}],
                    'buses': [{'time': '06:00 AM', 'cost': '¥2,500'}, {'time': '11:00 PM', 'cost': '¥2,500'}]
                },
                'nearby_attractions': [
                    {'name': 'Lake Kawaguchi', 'image': 'https://images.unsplash.com/photo-1528164344705-4754268799af'},
                    {'name': 'Arakurayama Sengen Park', 'image': 'https://images.unsplash.com/photo-1542051841857-5f90071e7989'}
                ]
            }
        ],
        'australia': [
            {
                'name': 'Sydney Opera House',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9',
                'description': 'A multi-venue performing arts centre in Sydney, one of the 20th century\'s most famous buildings.',
                'distance': '0 km from Sydney CBD',
                'best_time': 'September to November',
                'entry_fee': 'Free (walking around)',
                'famous_food': 'Barramundi, Pavlova',
                'suitability': ['Family', 'Couples'],
                'photo_spots': 'Mrs Macquarie\'s Chair.',
                'route': 'Train to Circular Quay.',
                'safety_tips': 'Wear sunscreen.',
                'budget': 'AUD 40 - AUD 120',
                'hotels': [
                    {'name': 'Park Hyatt Sydney', 'price': 'AUD 1,200', 'rating': '4.9'},
                    {'name': 'InterContinental Sydney', 'price': 'AUD 500', 'rating': '4.6'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': 'AUD 400'}, {'time': '07:00 PM', 'cost': 'AUD 550'}],
                    'trains': [{'time': '08:00 AM', 'cost': 'AUD 20'}, {'time': '10:00 PM', 'cost': 'AUD 20'}],
                    'buses': [{'time': '07:00 AM', 'cost': 'AUD 10'}, {'time': '11:00 PM', 'cost': 'AUD 10'}]
                },
                'nearby_attractions': [
                    {'name': 'Bondi Beach', 'image': 'https://images.unsplash.com/photo-1512428559087-560fa5ceab42'},
                    {'name': 'Sydney Harbour Bridge', 'image': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9'}
                ]
            }
        ],
        'indonesia': [
            {
                'name': 'Uluwatu Temple',
                'category': 'Temples',
                'image': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4',
                'description': 'A Balinese Hindu sea temple located in Uluwatu, built at the edge of a 70-meter high cliff.',
                'distance': '25 km from Kuta',
                'best_time': 'Sunset (Kecak Dance)',
                'entry_fee': 'IDR 50,000',
                'famous_food': 'Nasi Goreng, Sate Lilit',
                'suitability': ['Solo', 'Couples'],
                'photo_spots': 'The cliff edge view.',
                'route': 'Rent a scooter.',
                'safety_tips': 'Watch out for monkeys.',
                'budget': 'IDR 200k - 500k',
                'hotels': [
                    {'name': 'Alila Villas Uluwatu', 'price': 'IDR 12M', 'rating': '4.9'},
                    {'name': 'Radisson Blu Bali', 'price': 'IDR 3M', 'rating': '4.5'}
                ],
                'transport': {
                    'flights': [{'time': '10:00 AM', 'cost': 'IDR 1.2M'}, {'time': '06:00 PM', 'cost': 'IDR 1.5M'}],
                    'trains': [{'time': 'No Trains', 'cost': 'N/A'}],
                    'buses': [{'time': '08:00 AM', 'cost': 'IDR 50k'}, {'time': '10:00 PM', 'cost': 'IDR 50k'}]
                },
                'nearby_attractions': [
                    {'name': 'Padang Padang Beach', 'image': 'https://images.unsplash.com/photo-1539367628448-4bc5c9d171c8'},
                    {'name': 'Tegalalang Rice Terrace', 'image': 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2'}
                ]
            }
        ],
        'karnataka': [
            {
                'name': 'Hampi Ruins',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1600100397608-f09074aa8825',
                'description': 'A UNESCO World Heritage Site featuring the ruins of the Vijayanagara Empire.',
                'distance': '350 km from Bangalore',
                'best_time': 'October to February',
                'entry_fee': '₹40',
                'famous_food': 'Bisi Bele Bath, Filter Coffee',
                'suitability': ['History buffs', 'Solo'],
                'photo_spots': 'Virupaksha Temple at sunrise.',
                'route': 'Hampi Express Train.',
                'safety_tips': 'Wear comfortable shoes.',
                'budget': '₹1000 - ₹3000',
                'hotels': [
                    {'name': 'Evolve Back Hampi', 'price': '₹30,000', 'rating': '4.9'},
                    {'name': 'Heritage Resort Hampi', 'price': '₹8,000', 'rating': '4.4'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '₹4,500'}, {'time': '05:00 PM', 'cost': '₹5,500'}],
                    'trains': [{'time': '10:30 PM', 'cost': '₹800'}],
                    'buses': [{'time': '09:00 PM', 'cost': '₹1,200'}]
                },
                'nearby_attractions': [
                    {'name': 'Vittala Temple', 'image': 'https://images.unsplash.com/photo-1580966453127-9092d634289a'},
                    {'name': 'Matanga Hill', 'image': 'https://images.unsplash.com/photo-1589308078059-be1415eab4c3'}
                ]
            }
        ],
        'west bengal': [
            {
                'name': 'Victoria Memorial',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1558431382-27e303142255',
                'description': 'A large marble building in Kolkata, dedicated to the memory of Queen Victoria.',
                'distance': '0 km from Kolkata Center',
                'best_time': 'Evening (Light show)',
                'entry_fee': '₹30',
                'famous_food': 'Phuchka, Kathi Rolls',
                'suitability': ['Family', 'Couples'],
                'photo_spots': 'The front reflecting pool.',
                'route': 'Metro to Maidan.',
                'safety_tips': 'Visit early to avoid heat.',
                'budget': '₹200 - ₹500',
                'hotels': [
                    {'name': 'The Oberoi Grand', 'price': '₹12,000', 'rating': '4.8'},
                    {'name': 'ITC Sonar', 'price': '₹10,000', 'rating': '4.7'}
                ],
                'transport': {
                    'flights': [{'time': '08:00 AM', 'cost': '₹4,800'}, {'time': '06:00 PM', 'cost': '₹5,200'}],
                    'trains': [{'time': '07:00 AM', 'cost': '₹1,800'}, {'time': '11:00 PM', 'cost': '₹1,800'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹900'}, {'time': '10:00 PM', 'cost': '₹900'}]
                },
                'nearby_attractions': [
                    {'name': 'Howrah Bridge', 'image': 'https://images.unsplash.com/photo-1571679659147-33433c92889d'},
                    {'name': 'Dakshineswar Kali Temple', 'image': 'https://images.unsplash.com/photo-1598463510202-b2d28731737e'}
                ]
            }
        ],
        'gujarat': [
            {
                'name': 'Statue of Unity',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1579338559194-a162d19bf842',
                'description': 'The world\'s tallest statue, depicting Indian statesman Sardar Vallabhbhai Patel.',
                'distance': '90 km from Vadodara',
                'best_time': 'October to March',
                'entry_fee': '₹150',
                'famous_food': 'Dhokla, Khandvi',
                'suitability': ['Family', 'Friends'],
                'photo_spots': 'Viewing Gallery at 153m.',
                'route': 'Jan Shatabdi Express to Kevadia.',
                'safety_tips': 'Book gallery tickets online.',
                'budget': '₹500 - ₹1500',
                'hotels': [
                    {'name': 'Statue of Unity Tent City', 'price': '₹12,000', 'rating': '4.6'},
                    {'name': 'Ramada Encore', 'price': '₹6,000', 'rating': '4.3'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '₹4,200'}, {'time': '05:00 PM', 'cost': '₹4,200'}],
                    'trains': [{'time': '07:00 AM', 'cost': '₹600'}, {'time': '09:00 PM', 'cost': '₹600'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹300'}, {'time': '10:00 PM', 'cost': '₹300'}]
                },
                'nearby_attractions': [
                    {'name': 'Valley of Flowers', 'image': 'https://images.unsplash.com/photo-1469474968028-56623f02e42e'},
                    {'name': 'Sardar Sarovar Dam', 'image': 'https://images.unsplash.com/photo-1506477331477-33d5d8b3dc85'}
                ]
            }
        ],
        'assam': [
            {
                'name': 'Kaziranga National Park',
                'category': 'Nature',
                'image': 'https://images.unsplash.com/photo-1581007871115-f14bc016e0a4',
                'description': 'A UNESCO World Heritage site, home to two-thirds of the world\'s great one-horned rhinoceroses.',
                'distance': '200 km from Guwahati',
                'best_time': 'November to April',
                'entry_fee': '₹100 (Indians)',
                'famous_food': 'Masor Tenga',
                'suitability': ['Family', 'Nature lovers'],
                'photo_spots': 'Elephant Safari at sunrise.',
                'route': 'Bus/Cab from Guwahati.',
                'safety_tips': 'Follow guide instructions.',
                'budget': '₹2000 - ₹5000',
                'hotels': [
                    {'name': 'Borgos Resort', 'price': '₹8,000', 'rating': '4.7'},
                    {'name': 'Iora Retreat', 'price': '₹7,000', 'rating': '4.5'}
                ],
                'transport': {
                    'flights': [{'time': '10:00 AM', 'cost': '₹5,500'}, {'time': '04:00 PM', 'cost': '₹5,500'}],
                    'trains': [{'time': '06:00 AM', 'cost': '₹400'}],
                    'buses': [{'time': '07:00 AM', 'cost': '₹500'}]
                },
                'nearby_attractions': [
                    {'name': 'Orchid Park', 'image': 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad'},
                    {'name': 'Brahmaputra River', 'image': 'https://images.unsplash.com/photo-1623945415301-700140c83a73'}
                ]
            }
        ],
        'bihar': [
            {
                'name': 'Mahabodhi Temple',
                'category': 'Temples',
                'image': 'https://images.unsplash.com/photo-1622050290150-13f56d982189',
                'description': 'A UNESCO World Heritage Site where Siddhartha Gautama, the Buddha, attained enlightenment.',
                'distance': '100 km from Patna',
                'best_time': 'October to March',
                'entry_fee': 'Free',
                'famous_food': 'Litti Chokha',
                'suitability': ['Spiritual', 'Family'],
                'photo_spots': 'The Bodhi Tree.',
                'route': 'Train to Gaya Junction.',
                'safety_tips': 'Maintain silence.',
                'budget': '₹500 - ₹1500',
                'hotels': [
                    {'name': 'The Royal Residency', 'price': '₹6,000', 'rating': '4.4'},
                    {'name': 'Bodhgaya Regency', 'price': '₹5,000', 'rating': '4.3'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '₹4,800'}],
                    'trains': [{'time': '07:00 AM', 'cost': '₹300'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹200'}]
                },
                'nearby_attractions': [
                    {'name': 'Great Buddha Statue', 'image': 'https://images.unsplash.com/photo-1590732563939-2090f4236a04'},
                    {'name': 'Thai Monastery', 'image': 'https://images.unsplash.com/photo-1528127269322-539801943592'}
                ]
            }
        ],
        'punjab': [
            {
                'name': 'Golden Temple',
                'category': 'Temples',
                'image': 'https://images.unsplash.com/photo-1514222139-b57c44ce073b',
                'description': 'The preeminent spiritual site of Sikhism, famous for its full golden dome.',
                'distance': '0 km from Amritsar Center',
                'best_time': 'Early Morning',
                'entry_fee': 'Free',
                'famous_food': 'Amritsari Kulcha, Lassi',
                'suitability': ['Family', 'Spiritual'],
                'photo_spots': 'Reflection in the Sarovar.',
                'route': 'Amritsar Railway Station.',
                'safety_tips': 'Cover your head.',
                'budget': '₹200 - ₹1000',
                'hotels': [
                    {'name': 'Taj Swarna', 'price': '₹10,000', 'rating': '4.8'},
                    {'name': 'Hyatt Regency Amritsar', 'price': '₹8,000', 'rating': '4.7'}
                ],
                'transport': {
                    'flights': [{'time': '08:00 AM', 'cost': '₹4,500'}],
                    'trains': [{'time': '06:00 AM', 'cost': '₹1,200'}],
                    'buses': [{'time': '07:00 AM', 'cost': '₹800'}]
                },
                'nearby_attractions': [
                    {'name': 'Jallianwala Bagh', 'image': 'https://images.unsplash.com/photo-1589182373726-e4f658ab50f0'},
                    {'name': 'Wagah Border', 'image': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220'}
                ]
            }
        ],
        'uttar pradesh': [
            {
                'name': 'Taj Mahal',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1564507592333-c60657eea523',
                'description': 'An ivory-white marble mausoleum on the southern bank of the Yamuna river, one of the Seven Wonders.',
                'distance': '2 km from Agra Center',
                'best_time': 'Sunrise',
                'entry_fee': '₹50 (Indians)',
                'famous_food': 'Petha, Bedai',
                'suitability': ['Couples', 'Family'],
                'photo_spots': 'From the Diana Bench.',
                'route': 'Gatiman Express from Delhi.',
                'safety_tips': 'Hire authorized guides.',
                'budget': '₹500 - ₹2000',
                'hotels': [
                    {'name': 'The Oberoi Amarvilas', 'price': '₹40,000', 'rating': '5.0'},
                    {'name': 'ITC Mughal', 'price': '₹15,000', 'rating': '4.8'}
                ],
                'transport': {
                    'flights': [{'time': '10:00 AM', 'cost': '₹3,500'}],
                    'trains': [{'time': '08:00 AM', 'cost': '₹1,500'}],
                    'buses': [{'time': '07:00 AM', 'cost': '₹600'}]
                },
                'nearby_attractions': [
                    {'name': 'Agra Fort', 'image': 'https://images.unsplash.com/photo-1548013146-72479768bbaa'},
                    {'name': 'Fatehpur Sikri', 'image': 'https://images.unsplash.com/photo-1589308078059-be1415eab4c3'}
                ]
            }
        ],
        'odisha': [
            {
                'name': 'Konark Sun Temple',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1601961405399-800560e91aa8',
                'description': 'A 13th-century Sun Temple at Konark, designed as a colossal chariot of the Sun God.',
                'distance': '35 km from Puri',
                'best_time': 'October to March',
                'entry_fee': '₹40',
                'famous_food': 'Chhena Poda',
                'suitability': ['Family', 'History buffs'],
                'photo_spots': 'The giant stone wheels.',
                'route': 'Cab from Puri.',
                'safety_tips': 'Carry a water bottle.',
                'budget': '₹500 - ₹1500',
                'hotels': [
                    {'name': 'Mayfair Waves Puri', 'price': '₹12,000', 'rating': '4.7'},
                    {'name': 'Lotus Resort Konark', 'price': '₹6,000', 'rating': '4.3'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '₹5,200'}],
                    'trains': [{'time': '07:00 AM', 'cost': '₹600'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹300'}]
                },
                'nearby_attractions': [
                    {'name': 'Jagannath Temple', 'image': 'https://images.unsplash.com/photo-1600100397608-f09074aa8825'},
                    {'name': 'Chilika Lake', 'image': 'https://images.unsplash.com/photo-1598463510202-b2d28731737e'}
                ]
            }
        ],
        'madhya pradesh': [
            {
                'name': 'Khajuraho Temples',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1',
                'description': 'A UNESCO World Heritage site famous for its nagara-style architectural symbolism and erotic sculptures.',
                'distance': '10 km from Khajuraho Airport',
                'best_time': 'Winter',
                'entry_fee': '₹40',
                'famous_food': 'Bhutte Ka Kees',
                'suitability': ['Couples', 'History buffs'],
                'photo_spots': 'Kandariya Mahadev Temple.',
                'route': 'Khajuraho Railway Station.',
                'safety_tips': 'Respect local customs.',
                'budget': '₹1000 - ₹3000',
                'hotels': [
                    {'name': 'The Lalit Temple View', 'price': '₹12,000', 'rating': '4.7'},
                    {'name': 'Radisson Jass', 'price': '₹7,000', 'rating': '4.4'}
                ],
                'transport': {
                    'flights': [{'time': '11:00 AM', 'cost': '₹6,200'}],
                    'trains': [{'time': '08:00 AM', 'cost': '₹1,200'}],
                    'buses': [{'time': '07:00 AM', 'cost': '₹800'}]
                },
                'nearby_attractions': [
                    {'name': 'Panna National Park', 'image': 'https://images.unsplash.com/photo-1581007871115-f14bc016e0a4'},
                    {'name': 'Raneh Falls', 'image': 'https://images.unsplash.com/photo-1506477331477-33d5d8b3dc85'}
                ]
            }
        ],
        'andhra pradesh': [
            {
                'name': 'Tirumala Venkateswara Temple',
                'category': 'Temples',
                'image': 'https://images.unsplash.com/photo-1622050290150-13f56d982189',
                'description': 'One of the most visited holy places in the world, dedicated to Lord Venkateswara.',
                'distance': '20 km from Tirupati',
                'best_time': 'September to March',
                'entry_fee': 'Free (Special entry ₹300)',
                'famous_food': 'Tirupati Laddu',
                'suitability': ['Family', 'Spiritual'],
                'photo_spots': 'Main Temple Entrance.',
                'route': 'Bus/Walk from Tirupati.',
                'safety_tips': 'Follow queue system.',
                'budget': '₹500 - ₹2000',
                'hotels': [
                    {'name': 'Taj Tirupati', 'price': '₹9,000', 'rating': '4.8'},
                    {'name': 'Fortune Select Grand', 'price': '₹6,000', 'rating': '4.5'}
                ],
                'transport': {
                    'flights': [{'time': '09:00 AM', 'cost': '₹4,500'}],
                    'trains': [{'time': '07:00 AM', 'cost': '₹500'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹300'}]
                },
                'nearby_attractions': [
                    {'name': 'Akasaganga Teertham', 'image': 'https://images.unsplash.com/photo-1506477331477-33d5d8b3dc85'},
                    {'name': 'Silathoranam', 'image': 'https://images.unsplash.com/photo-1542385151-efd9000785a0'}
                ]
            }
        ],
        'telangana': [
            {
                'name': 'Charminar',
                'category': 'Historical',
                'image': 'https://images.unsplash.com/photo-1599402513904-807e15d8f6d8',
                'description': 'A mosque and monument built in 1591, widely recognized as a symbol of Hyderabad.',
                'distance': '0 km from Old City Hyderabad',
                'best_time': 'Evening',
                'entry_fee': '₹25',
                'famous_food': 'Hyderabadi Biryani',
                'suitability': ['Family', 'Foodies'],
                'photo_spots': 'Top floor arch view.',
                'route': 'Auto/Metro to MGBS.',
                'safety_tips': 'Watch out for heavy traffic.',
                'budget': '₹200 - ₹800',
                'hotels': [
                    {'name': 'Taj Falaknuma Palace', 'price': '₹50,000', 'rating': '5.0'},
                    {'name': 'Park Hyatt Hyderabad', 'price': '₹15,000', 'rating': '4.8'}
                ],
                'transport': {
                    'flights': [{'time': '08:00 AM', 'cost': '₹5,200'}],
                    'trains': [{'time': '07:00 AM', 'cost': '₹1,200'}],
                    'buses': [{'time': '06:00 AM', 'cost': '₹800'}]
                },
                'nearby_attractions': [
                    {'name': 'Golconda Fort', 'image': 'https://images.unsplash.com/photo-1548013146-72479768bbaa'},
                    {'name': 'Salar Jung Museum', 'image': 'https://images.unsplash.com/photo-1589308078059-be1415eab4c3'}
                ]
            }
        ],
        'chhattisgarh': [
            {
                'name': 'Chitrakoot Falls',
                'category': 'Nature',
                'image': 'https://images.unsplash.com/photo-1506477331477-33d5d8b3dc85',
                'description': 'Often called the Niagara Falls of India, it is the widest waterfall in the country.',
                'distance': '38 km from Jagdalpur',
                'best_time': 'July to October (Monsoon)',
                'entry_fee': 'Free',
                'famous_food': 'Bastar cuisine',
                'suitability': ['Nature lovers', 'Family'],
                'photo_spots': 'The Horseshoe view.',
                'route': 'Cab from Jagdalpur.',
                'safety_tips': 'Keep distance from edges.',
                'budget': '₹500 - ₹1500',
                'hotels': [
                    {'name': 'Dandami Luxury Resort', 'price': '₹5,000', 'rating': '4.3'}
                ],
                'transport': {
                    'flights': [{'time': '10:00 AM', 'cost': '₹4,800'}],
                    'trains': [{'time': '08:00 AM', 'cost': '₹600'}],
                    'buses': [{'time': '07:00 AM', 'cost': '₹400'}]
                },
                'nearby_attractions': [
                    {'name': 'Tirathgarh Falls', 'image': 'https://images.unsplash.com/photo-1506477331477-33d5d8b3dc85'},
                    {'name': 'Kanger Valley National Park', 'image': 'https://images.unsplash.com/photo-1581007871115-f14bc016e0a4'}
                ]
            }
        ]
    }

    @classmethod
    def get_local_recommendations(cls, location, category='All'):
        city = location.lower().strip()
        data = cls.HUBS.get(city, [])
        
        if not data:
            # Map countries to their primary hubs
            if city in ['uk', 'united kingdom', 'britain']:
                data = cls.HUBS.get('london', [])
            elif city in ['usa', 'united states', 'america', 'us']:
                data = cls.HUBS.get('usa', [])
            elif city in ['japan']:
                data = cls.HUBS.get('tokyo', []) or cls.HUBS.get('japan', [])
            elif city in ['france']:
                data = cls.HUBS.get('france', [])
            elif city in ['italy']:
                data = cls.HUBS.get('italy', [])
            elif city in ['india']:
                # Combine major Indian hubs
                data = (cls.HUBS.get('delhi', []) + cls.HUBS.get('mumbai', []) + 
                        cls.HUBS.get('kerala', []) + cls.HUBS.get('goa', []))
        
        if not data:
            # Simple fuzzy search if exact match fails
            for hub_city, hub_data in cls.HUBS.items():
                if city in hub_city or hub_city in city:
                    data = hub_data
                    break
        
        if not data:
            # Smart Fallback: Generate a "Smart Guide" if no hardcoded data exists
            data = [{
                'name': f'Discover {location}',
                'category': 'Exploration',
                'image': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828',
                'description': f'Uncover the hidden gems, local culture, and stunning landscapes of {location}. A unique destination waiting to be explored.',
                'distance': 'Variable',
                'best_time': 'October to March',
                'entry_fee': 'Variable',
                'famous_food': 'Local Traditional Cuisine',
                'suitability': ['Adventurers', 'Solo Travelers'],
                'photo_spots': 'Main Town Square / Viewpoints.',
                'route': f'Direct flights/trains to {location} center.',
                'safety_tips': 'Always check local weather and guides.',
                'budget': 'Variable',
                'hotels': [
                    {'name': f'{location} Grand Hotel', 'price': '₹5,000', 'rating': '4.5'},
                    {'name': f'The {location} Heritage', 'price': '₹3,500', 'rating': '4.2'}
                ],
                'transport': {
                    'flights': [{'time': 'Flexible', 'cost': 'Check App'}],
                    'trains': [{'time': 'Flexible', 'cost': 'Check App'}],
                    'buses': [{'time': 'Flexible', 'cost': 'Check App'}]
                },
                'nearby_attractions': [
                    {'name': 'Main City Landmark', 'image': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828'},
                    {'name': 'Nature Park', 'image': 'https://images.unsplash.com/photo-1469474968028-56623f02e42e'}
                ]
            }]
            
        if category != 'All':
            data = [p for p in data if p['category'] == category]
            
        return data

    @classmethod
    def search_places(cls, query):
        query = query.lower().strip()
        results = []
        for city, places in cls.HUBS.items():
            if query in city:
                results.extend(places)
            else:
                for place in places:
                    if query in place['name'].lower() or query in place['category'].lower() or query in place['description'].lower():
                        results.append(place)
        
        # If no hardcoded results, generate a "smart" response for global discovery
        if not results:
            # Mocking world-wide discovery
            if 'japan' in query:
                results = cls.HUBS.get('tokyo')
            elif 'usa' in query or 'america' in query:
                results = cls.HUBS.get('new york')
            elif 'uk' in query or 'britain' in query:
                results = cls.HUBS.get('london')
            elif 'india' in query:
                results = cls.HUBS.get('delhi') + cls.HUBS.get('rajasthan') + cls.HUBS.get('kerala') + cls.HUBS.get('goa')
            elif 'kerala' in query:
                results = cls.HUBS.get('kerala')
            elif 'goa' in query:
                results = cls.HUBS.get('goa')
            elif 'himachal' in query:
                results = cls.HUBS.get('himachal')
            elif 'rajasthan' in query:
                results = cls.HUBS.get('rajasthan')
            elif 'tamil nadu' in query:
                results = cls.HUBS.get('tamil nadu')
        
        return results


class TravelAI:
    @staticmethod
    def predict_cost(duration, scope, travel_type):
        base_per_day = 100 if scope == 'Inside India' else 350
        
        type_multipliers = {
            'Solo': 1.0,
            'Family': 2.5,
            'Adventure': 1.5,
            'Romantic': 2.0,
            'Business': 2.2
        }
        
        multiplier = type_multipliers.get(travel_type, 1.0)
        estimated_min = base_per_day * duration * multiplier
        
        category = "Budget-friendly"
        if estimated_min > 5000:
            category = "Expensive"
        elif estimated_min > 2000:
            category = "Moderate"
            
        return {
            'estimated_min': int(estimated_min),
            'category': category,
            'per_day': int(estimated_min / duration)
        }

    @staticmethod
    def generate_itinerary(destination, duration, travel_type, budget, scope='Inside India'):
        activities_pool = {
            'Solo': ['Backpacking through old streets', 'Visiting local cafes', 'Photography tour', 'Hiking', 'Meditation'],
            'Family': ['Theme park visit', 'Museum tour', 'Beach day', 'Zoo visit', 'Family dinner'],
            'Adventure': ['Bungee jumping', 'Scuba diving', 'Mountain climbing', 'Jungle safari', 'River rafting'],
            'Romantic': ['Candlelight dinner', 'Sunset cruise', 'Wine tasting', 'Couple spa', 'Star gazing'],
            'Business': ['Networking event', 'City tour', 'High-end dining', 'Visiting landmarks', 'Local market visit']
        }
        
        itinerary_data = []
        daily_budget = float(budget) / duration
        
        for i in range(1, duration + 1):
            day_activities = random.sample(activities_pool.get(travel_type, activities_pool['Solo']), 2)
            itinerary_data.append({
                'day': i,
                'activities': ", ".join(day_activities),
                'meals': "Breakfast at hotel, Lunch at local diner, Dinner at " + random.choice(['City Center', 'Harbor View', 'Sky Lounge']),
                'expenses': round(daily_budget * 0.8, 2)
            })
        return itinerary_data

# --- Auth Views ---

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'travel_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'travel_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- Core Logic Views ---

def home(request):
    featured_destinations = [
        {'name': 'Paris, France', 'image': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34', 'price': 1200, 'rating': 4.8},
        {'name': 'Bali, Indonesia', 'image': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4', 'price': 800, 'rating': 4.7},
        {'name': 'Tokyo, Japan', 'image': 'https://images.unsplash.com/photo-1540959733332-e9ab659b8120', 'price': 1500, 'rating': 4.9},
        {'name': 'Santorini, Greece', 'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff', 'price': 1100, 'rating': 4.8},
    ]
    return render(request, 'travel_app/home.html', {'destinations': featured_destinations})

@login_required
def dashboard(request):
    user_trips = Trip.objects.filter(user=request.user)
    total_trips = user_trips.count()

    # Count unique destinations from the user's trips
    total_places = user_trips.values('destination_name').distinct().count()

    # Count actual saved items from the SavedTrip model
    total_saved = SavedTrip.objects.filter(user=request.user).count()

    recent_trips = user_trips.order_by('-created_at')[:5]
    recent_places = RecentPlace.objects.filter(user=request.user).order_by('-visited_at')[:5]

    return render(request, 'travel_app/dashboard.html', {
        'recent_trips': recent_trips,
        'recent_places': recent_places,
        'total_trips': total_trips,
        'total_places': total_places,
        'total_saved': total_saved,
    })

@login_required
def ai_planner(request):
    initial_data = {}
    if request.method == 'GET':
        dest = request.GET.get('destination')
        scope = request.GET.get('scope')
        if dest:
            initial_data['destination'] = dest
        if scope:
            initial_data['trip_scope'] = scope
            
    if request.method == 'POST':
        form = TripPlannerForm(request.POST)
        if form.is_valid():
            dest = form.cleaned_data['destination']
            start_p = form.cleaned_data['starting_point']
            budget = form.cleaned_data['budget']
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            t_type = form.cleaned_data['travel_type']
            scope = form.cleaned_data['trip_scope']
            
            # Create Trip
            trip = Trip.objects.create(
                user=request.user,
                starting_point=start_p,
                destination_name=dest,
                budget=budget,
                start_date=start,
                end_date=end,
                travel_type=t_type
            )
            
            # Record Recent Place
            RecentPlace.objects.create(user=request.user, place_name=dest)
            
            # Generate AI Itinerary
            duration = (end - start).days + 1
            itinerary_data = TravelAI.generate_itinerary(dest, duration, t_type, budget, scope)
            
            for item in itinerary_data:
                Itinerary.objects.create(
                    trip=trip,
                    day_number=item['day'],
                    activities=item['activities'],
                    meals=item['meals'],
                    expenses_estimate=item['expenses']
                )
            
            return redirect('itinerary_detail', trip_id=trip.id)
    else:
        form = TripPlannerForm(initial=initial_data)
    return render(request, 'travel_app/planner.html', {'form': form, 'indian_states': INDIAN_STATES})

@login_required
def itinerary_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    itineraries = trip.itineraries.all()
    total_estimated = sum(i.expenses_estimate for i in itineraries)
    is_saved = SavedTrip.objects.filter(user=request.user, trip_data__trip_id=trip_id).exists()
    return render(request, 'travel_app/itinerary_detail.html', {
        'trip': trip,
        'itineraries': itineraries,
        'total_estimated': total_estimated,
        'is_saved': is_saved,
    })

@login_required
def hotel_recommendations(request, trip_id=None):
    hotels = [
        {'name': 'Grand Plaza Hotel', 'location': 'City Center', 'price': 150, 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945'},
        {'name': 'Ocean View Resort', 'location': 'Beachfront', 'price': 250, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4'},
        {'name': 'Mountain Retreat', 'location': 'Highlands', 'price': 180, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1445019980597-93fa8acb246c'},
        {'name': 'Urban Boutique', 'location': 'Downtown', 'price': 120, 'rating': 4.2, 'image': 'https://images.unsplash.com/photo-1551882547-ff43c63be5c2'},
    ]
    trip = None
    if trip_id:
        trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    return render(request, 'travel_app/hotels.html', {'hotels': hotels, 'trip': trip})

@login_required
def payment_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Simulate Payment
            Payment.objects.create(
                trip=trip,
                amount=trip.budget,
                transaction_id=str(uuid.uuid4()).split('-')[0].upper()
            )
            messages.success(request, "Payment successful! Your trip is booked.")
            return redirect('invoice', trip_id=trip.id)
    else:
        form = PaymentForm()
    
    selected_hotel = request.GET.get('hotel')
    return render(request, 'travel_app/payment.html', {
        'form': form, 
        'trip': trip,
        'selected_hotel': selected_hotel
    })

@login_required
def invoice_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    payment = Payment.objects.filter(trip=trip).last()
    if not payment:
        messages.error(request, "Please complete the payment first.")
        return redirect('payment', trip_id=trip.id)
    itineraries = trip.itineraries.all()
    return render(request, 'travel_app/invoice.html', {
        'trip': trip,
        'payment': payment,
        'itineraries': itineraries
    })

@login_required
def saved_trips(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'travel_app/saved_trips.html', {'trips': trips})

@login_required
def save_trip_toggle(request, trip_id):
    """Toggle saving/unsaving a trip to the user's Saved Items."""
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    existing = SavedTrip.objects.filter(user=request.user, trip_data__trip_id=trip_id)
    if existing.exists():
        existing.delete()
        saved = False
    else:
        SavedTrip.objects.create(
            user=request.user,
            trip_data={
                'trip_id': trip_id,
                'destination': trip.destination_name,
                'start_date': str(trip.start_date),
                'end_date': str(trip.end_date),
                'budget': str(trip.budget),
                'travel_type': trip.travel_type,
                'duration': trip.duration,
            }
        )
        saved = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved})
    return redirect('itinerary_detail', trip_id=trip_id)

@login_required
def saved_items_view(request):
    """Show all trips the user has explicitly saved."""
    saved = SavedTrip.objects.filter(user=request.user).order_by('-saved_at')
    return render(request, 'travel_app/saved_items.html', {'saved_items': saved})

@login_required
def destinations_view(request):
    """Show all unique destinations across the user's trips."""
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    # Group by destination name, keep the most recent trip per destination
    seen = set()
    unique_destinations = []
    for trip in trips:
        if trip.destination_name not in seen:
            seen.add(trip.destination_name)
            unique_destinations.append(trip)
    return render(request, 'travel_app/destinations.html', {
        'destinations': unique_destinations,
        'total': len(unique_destinations),
    })

@login_required
def delete_destination(request, destination_name):
    """Delete all trips and recent place records for a specific destination."""
    Trip.objects.filter(user=request.user, destination_name=destination_name).delete()
    RecentPlace.objects.filter(user=request.user, place_name=destination_name).delete()
    messages.success(request, f"Removed {destination_name} from your explored destinations.")
    return redirect('destinations')

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid():
            p_form.save()
            # Also update user email if needed (simple version)
            email = request.POST.get('email')
            if email:
                request.user.email = email
                request.user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        p_form = UserProfileForm(instance=profile)
    return render(request, 'travel_app/profile.html', {'p_form': p_form})

@login_required
def chatbot_view(request):
    return render(request, 'travel_app/chatbot.html')

def chatbot_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').lower()
        
        responses = [
            "That's a great question! I recommend visiting Paris for its romantic vibes.",
            "If you're on a budget, Bali is an excellent choice.",
            "For adventure seekers, Tokyo offers amazing urban exploration.",
            "I can help you plan your next trip! Just use the AI Planner.",
            "The best time to travel is usually during the shoulder season to save costs."
        ]
        
        if 'budget' in user_message:
            reply = "To stay within budget, try booking hostels and eating at local markets."
        elif 'place' in user_message or 'destination' in user_message:
            reply = "Top destinations right now include Switzerland, Bali, and New York."
        else:
            reply = random.choice(responses)
            
        return JsonResponse({'reply': reply})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def discover_view(request):
    location = request.GET.get('location', 'Delhi')
    category = request.GET.get('category', 'All')
    recommendations = DiscoveryAI.get_local_recommendations(location, category)
    
    countries = [
        'India', 'USA', 'UK', 'France', 'Italy', 'Japan', 'Indonesia', 'Switzerland', 'Australia', 'Canada'
    ]
    
    context = {
        'location': location,
        'category': category,
        'recommendations': recommendations,
        'categories': ['All', 'Historical', 'Nature', 'Temples', 'Adventure', 'Hidden gems', 'Food spots'],
        'indian_states': INDIAN_STATES,
        'countries': sorted(countries)
    }
    return render(request, 'travel_app/discover.html', context)

@login_required
def discovery_bot_api(request):
    if request.method == 'POST':
        query = request.POST.get('message', '').lower()
        
        if not query:
            return JsonResponse({'reply': 'I am your AI Discovery Bot! How can I help you find your next destination?'})
        
        # Search for places
        places = DiscoveryAI.search_places(query)
        
        if places:
            reply = f"I found some amazing spots for you! Check these out:"
            return JsonResponse({
                'reply': reply,
                'places': places[:3] # Return top 3
            })
        else:
            return JsonResponse({
                'reply': "I couldn't find specific spots for that, but you should explore places like Tokyo, Paris, or Kerala! Would you like me to tell you more about them?"
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

# --- Seasonal Discovery Feature ---

SEASONAL_DATA = {
    'Summer': {
        'India': [
            {'name': 'Manali', 'description': 'Cool mountain air and adventure sports.', 'image': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23'},
            {'name': 'Leh Ladakh', 'description': 'The land of high passes and stunning lakes.', 'image': 'https://images.unsplash.com/photo-1581791534721-e599df4417f7'},
            {'name': 'Munnar', 'description': 'Lush tea gardens and misty hills.', 'image': 'https://images.unsplash.com/photo-1593693397690-362cb9666fc2'},
        ],
        'Foreign': [
            {'name': 'Switzerland', 'description': 'Pristine Alps and crystal clear lakes.', 'image': 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99'},
            {'name': 'Iceland', 'description': 'Midnight sun and dramatic landscapes.', 'image': 'https://images.unsplash.com/photo-1520637102912-2df6bb2aec6d'},
            {'name': 'Norway', 'description': 'Breathtaking fjords and summer hiking.', 'image': 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd'},
        ]
    },
    'Winter': {
        'India': [
            {'name': 'Gulmarg', 'description': 'The winter wonderland for skiing.', 'image': 'https://images.unsplash.com/photo-1548013146-72479768bbaa'},
            {'name': 'Jaisalmer', 'description': 'Golden sands and desert safaris.', 'image': 'https://images.unsplash.com/photo-1589182337358-2cb63099350c'},
            {'name': 'Auli', 'description': 'India\'s premier skiing destination.', 'image': 'https://images.unsplash.com/photo-1586944210611-f1f456184a5a'},
        ],
        'Foreign': [
            {'name': 'Lapland, Finland', 'description': 'Santa Claus village and Northern Lights.', 'image': 'https://images.unsplash.com/photo-1517154421773-0529f29ea451'},
            {'name': 'Japan', 'description': 'World-class skiing and onsen retreats.', 'image': 'https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d'},
            {'name': 'Banff, Canada', 'description': 'Stunning Rocky Mountains in the snow.', 'image': 'https://images.unsplash.com/photo-1502444330042-d1a1ddf9bb5b'},
        ]
    },
    'Rainy': {
        'India': [
            {'name': 'Cherrapunji', 'description': 'The wettest place on earth with living bridges.', 'image': 'https://images.unsplash.com/photo-1581446714041-39626e2e5491'},
            {'name': 'Wayanad', 'description': 'Refreshing greenery and waterfalls.', 'image': 'https://images.unsplash.com/photo-1627393100177-b4297e79a5be'},
            {'name': 'Lonavala', 'description': 'Monsoon paradise near Mumbai.', 'image': 'https://images.unsplash.com/photo-1518173946687-a4c8a9833786'},
        ],
        'Foreign': [
            {'name': 'Costa Rica', 'description': 'Lush rainforests in the green season.', 'image': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23'},
            {'name': 'Bali, Indonesia', 'description': 'Tropical rains and vibrant landscapes.', 'image': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4'},
            {'name': 'Vietnam', 'description': 'Emerald rice paddies during monsoon.', 'image': 'https://images.unsplash.com/photo-1528127269322-539801943592'},
        ]
    }
}

@login_required
def seasonal_guide(request):
    season = request.GET.get('season', 'Summer')
    region = request.GET.get('region', 'India')
    
    recommendations = SEASONAL_DATA.get(season, {}).get(region, [])
    
    context = {
        'selected_season': season,
        'selected_region': region,
        'recommendations': recommendations,
        'seasons': ['Summer', 'Winter', 'Rainy'],
        'regions': ['India', 'Foreign']
    }
    return render(request, 'travel_app/seasonal_guide.html', context)
