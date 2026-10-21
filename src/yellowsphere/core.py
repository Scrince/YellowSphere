                      
                                                                       

import base64
import csv
import hashlib
import hmac
import io
import json
import os
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Tuple
from urllib.parse import quote


APP_VERSION = "1.6.6"


                                          
BIP39_WORDS = [
    'abandon',
    'ability',
    'able',
    'about',
    'above',
    'absent',
    'absorb',
    'abstract',
    'absurd',
    'abuse',
    'access',
    'accident',
    'account',
    'accuse',
    'achieve',
    'acid',
    'acoustic',
    'acquire',
    'across',
    'act',
    'action',
    'actor',
    'actress',
    'actual',
    'adapt',
    'add',
    'addict',
    'address',
    'adjust',
    'admit',
    'adult',
    'advance',
    'advice',
    'aerobic',
    'affair',
    'afford',
    'afraid',
    'again',
    'age',
    'agent',
    'agree',
    'ahead',
    'aim',
    'air',
    'airport',
    'aisle',
    'alarm',
    'album',
    'alcohol',
    'alert',
    'alien',
    'all',
    'alley',
    'allow',
    'almost',
    'alone',
    'alpha',
    'already',
    'also',
    'alter',
    'always',
    'amateur',
    'amazing',
    'among',
    'amount',
    'amused',
    'analyst',
    'anchor',
    'ancient',
    'anger',
    'angle',
    'angry',
    'animal',
    'ankle',
    'announce',
    'annual',
    'another',
    'answer',
    'antenna',
    'antique',
    'anxiety',
    'any',
    'apart',
    'apology',
    'appear',
    'apple',
    'approve',
    'april',
    'arch',
    'arctic',
    'area',
    'arena',
    'argue',
    'arm',
    'armed',
    'armor',
    'army',
    'around',
    'arrange',
    'arrest',
    'arrive',
    'arrow',
    'art',
    'artefact',
    'artist',
    'artwork',
    'ask',
    'aspect',
    'assault',
    'asset',
    'assist',
    'assume',
    'asthma',
    'athlete',
    'atom',
    'attack',
    'attend',
    'attitude',
    'attract',
    'auction',
    'audit',
    'august',
    'aunt',
    'author',
    'auto',
    'autumn',
    'average',
    'avocado',
    'avoid',
    'awake',
    'aware',
    'away',
    'awesome',
    'awful',
    'awkward',
    'axis',
    'baby',
    'bachelor',
    'bacon',
    'badge',
    'bag',
    'balance',
    'balcony',
    'ball',
    'bamboo',
    'banana',
    'banner',
    'bar',
    'barely',
    'bargain',
    'barrel',
    'base',
    'basic',
    'basket',
    'battle',
    'beach',
    'bean',
    'beauty',
    'because',
    'become',
    'beef',
    'before',
    'begin',
    'behave',
    'behind',
    'believe',
    'below',
    'belt',
    'bench',
    'benefit',
    'best',
    'betray',
    'better',
    'between',
    'beyond',
    'bicycle',
    'bid',
    'bike',
    'bind',
    'biology',
    'bird',
    'birth',
    'bitter',
    'black',
    'blade',
    'blame',
    'blanket',
    'blast',
    'bleak',
    'bless',
    'blind',
    'blood',
    'blossom',
    'blouse',
    'blue',
    'blur',
    'blush',
    'board',
    'boat',
    'body',
    'boil',
    'bomb',
    'bone',
    'bonus',
    'book',
    'boost',
    'border',
    'boring',
    'borrow',
    'boss',
    'bottom',
    'bounce',
    'box',
    'boy',
    'bracket',
    'brain',
    'brand',
    'brass',
    'brave',
    'bread',
    'breeze',
    'brick',
    'bridge',
    'brief',
    'bright',
    'bring',
    'brisk',
    'broccoli',
    'broken',
    'bronze',
    'broom',
    'brother',
    'brown',
    'brush',
    'bubble',
    'buddy',
    'budget',
    'buffalo',
    'build',
    'bulb',
    'bulk',
    'bullet',
    'bundle',
    'bunker',
    'burden',
    'burger',
    'burst',
    'bus',
    'business',
    'busy',
    'butter',
    'buyer',
    'buzz',
    'cabbage',
    'cabin',
    'cable',
    'cactus',
    'cage',
    'cake',
    'call',
    'calm',
    'camera',
    'camp',
    'can',
    'canal',
    'cancel',
    'candy',
    'cannon',
    'canoe',
    'canvas',
    'canyon',
    'capable',
    'capital',
    'captain',
    'car',
    'carbon',
    'card',
    'cargo',
    'carpet',
    'carry',
    'cart',
    'case',
    'cash',
    'casino',
    'castle',
    'casual',
    'cat',
    'catalog',
    'catch',
    'category',
    'cattle',
    'caught',
    'cause',
    'caution',
    'cave',
    'ceiling',
    'celery',
    'cement',
    'census',
    'century',
    'cereal',
    'certain',
    'chair',
    'chalk',
    'champion',
    'change',
    'chaos',
    'chapter',
    'charge',
    'chase',
    'chat',
    'cheap',
    'check',
    'cheese',
    'chef',
    'cherry',
    'chest',
    'chicken',
    'chief',
    'child',
    'chimney',
    'choice',
    'choose',
    'chronic',
    'chuckle',
    'chunk',
    'churn',
    'cigar',
    'cinnamon',
    'circle',
    'citizen',
    'city',
    'civil',
    'claim',
    'clap',
    'clarify',
    'claw',
    'clay',
    'clean',
    'clerk',
    'clever',
    'click',
    'client',
    'cliff',
    'climb',
    'clinic',
    'clip',
    'clock',
    'clog',
    'close',
    'cloth',
    'cloud',
    'clown',
    'club',
    'clump',
    'cluster',
    'clutch',
    'coach',
    'coast',
    'coconut',
    'code',
    'coffee',
    'coil',
    'coin',
    'collect',
    'color',
    'column',
    'combine',
    'come',
    'comfort',
    'comic',
    'common',
    'company',
    'concert',
    'conduct',
    'confirm',
    'congress',
    'connect',
    'consider',
    'control',
    'convince',
    'cook',
    'cool',
    'copper',
    'copy',
    'coral',
    'core',
    'corn',
    'correct',
    'cost',
    'cotton',
    'couch',
    'country',
    'couple',
    'course',
    'cousin',
    'cover',
    'coyote',
    'crack',
    'cradle',
    'craft',
    'cram',
    'crane',
    'crash',
    'crater',
    'crawl',
    'crazy',
    'cream',
    'credit',
    'creek',
    'crew',
    'cricket',
    'crime',
    'crisp',
    'critic',
    'crop',
    'cross',
    'crouch',
    'crowd',
    'crucial',
    'cruel',
    'cruise',
    'crumble',
    'crunch',
    'crush',
    'cry',
    'crystal',
    'cube',
    'culture',
    'cup',
    'cupboard',
    'curious',
    'current',
    'curtain',
    'curve',
    'cushion',
    'custom',
    'cute',
    'cycle',
    'dad',
    'damage',
    'damp',
    'dance',
    'danger',
    'daring',
    'dash',
    'daughter',
    'dawn',
    'day',
    'deal',
    'debate',
    'debris',
    'decade',
    'december',
    'decide',
    'decline',
    'decorate',
    'decrease',
    'deer',
    'defense',
    'define',
    'defy',
    'degree',
    'delay',
    'deliver',
    'demand',
    'demise',
    'denial',
    'dentist',
    'deny',
    'depart',
    'depend',
    'deposit',
    'depth',
    'deputy',
    'derive',
    'describe',
    'desert',
    'design',
    'desk',
    'despair',
    'destroy',
    'detail',
    'detect',
    'develop',
    'device',
    'devote',
    'diagram',
    'dial',
    'diamond',
    'diary',
    'dice',
    'diesel',
    'diet',
    'differ',
    'digital',
    'dignity',
    'dilemma',
    'dinner',
    'dinosaur',
    'direct',
    'dirt',
    'disagree',
    'discover',
    'disease',
    'dish',
    'dismiss',
    'disorder',
    'display',
    'distance',
    'divert',
    'divide',
    'divorce',
    'dizzy',
    'doctor',
    'document',
    'dog',
    'doll',
    'dolphin',
    'domain',
    'donate',
    'donkey',
    'donor',
    'door',
    'dose',
    'double',
    'dove',
    'draft',
    'dragon',
    'drama',
    'drastic',
    'draw',
    'dream',
    'dress',
    'drift',
    'drill',
    'drink',
    'drip',
    'drive',
    'drop',
    'drum',
    'dry',
    'duck',
    'dumb',
    'dune',
    'during',
    'dust',
    'dutch',
    'duty',
    'dwarf',
    'dynamic',
    'eager',
    'eagle',
    'early',
    'earn',
    'earth',
    'easily',
    'east',
    'easy',
    'echo',
    'ecology',
    'economy',
    'edge',
    'edit',
    'educate',
    'effort',
    'egg',
    'eight',
    'either',
    'elbow',
    'elder',
    'electric',
    'elegant',
    'element',
    'elephant',
    'elevator',
    'elite',
    'else',
    'embark',
    'embody',
    'embrace',
    'emerge',
    'emotion',
    'employ',
    'empower',
    'empty',
    'enable',
    'enact',
    'end',
    'endless',
    'endorse',
    'enemy',
    'energy',
    'enforce',
    'engage',
    'engine',
    'enhance',
    'enjoy',
    'enlist',
    'enough',
    'enrich',
    'enroll',
    'ensure',
    'enter',
    'entire',
    'entry',
    'envelope',
    'episode',
    'equal',
    'equip',
    'era',
    'erase',
    'erode',
    'erosion',
    'error',
    'erupt',
    'escape',
    'essay',
    'essence',
    'estate',
    'eternal',
    'ethics',
    'evidence',
    'evil',
    'evoke',
    'evolve',
    'exact',
    'example',
    'excess',
    'exchange',
    'excite',
    'exclude',
    'excuse',
    'execute',
    'exercise',
    'exhaust',
    'exhibit',
    'exile',
    'exist',
    'exit',
    'exotic',
    'expand',
    'expect',
    'expire',
    'explain',
    'expose',
    'express',
    'extend',
    'extra',
    'eye',
    'eyebrow',
    'fabric',
    'face',
    'faculty',
    'fade',
    'faint',
    'faith',
    'fall',
    'false',
    'fame',
    'family',
    'famous',
    'fan',
    'fancy',
    'fantasy',
    'farm',
    'fashion',
    'fat',
    'fatal',
    'father',
    'fatigue',
    'fault',
    'favorite',
    'feature',
    'february',
    'federal',
    'fee',
    'feed',
    'feel',
    'female',
    'fence',
    'festival',
    'fetch',
    'fever',
    'few',
    'fiber',
    'fiction',
    'field',
    'figure',
    'file',
    'film',
    'filter',
    'final',
    'find',
    'fine',
    'finger',
    'finish',
    'fire',
    'firm',
    'first',
    'fiscal',
    'fish',
    'fit',
    'fitness',
    'fix',
    'flag',
    'flame',
    'flash',
    'flat',
    'flavor',
    'flee',
    'flight',
    'flip',
    'float',
    'flock',
    'floor',
    'flower',
    'fluid',
    'flush',
    'fly',
    'foam',
    'focus',
    'fog',
    'foil',
    'fold',
    'follow',
    'food',
    'foot',
    'force',
    'forest',
    'forget',
    'fork',
    'fortune',
    'forum',
    'forward',
    'fossil',
    'foster',
    'found',
    'fox',
    'fragile',
    'frame',
    'frequent',
    'fresh',
    'friend',
    'fringe',
    'frog',
    'front',
    'frost',
    'frown',
    'frozen',
    'fruit',
    'fuel',
    'fun',
    'funny',
    'furnace',
    'fury',
    'future',
    'gadget',
    'gain',
    'galaxy',
    'gallery',
    'game',
    'gap',
    'garage',
    'garbage',
    'garden',
    'garlic',
    'garment',
    'gas',
    'gasp',
    'gate',
    'gather',
    'gauge',
    'gaze',
    'general',
    'genius',
    'genre',
    'gentle',
    'genuine',
    'gesture',
    'ghost',
    'giant',
    'gift',
    'giggle',
    'ginger',
    'giraffe',
    'girl',
    'give',
    'glad',
    'glance',
    'glare',
    'glass',
    'glide',
    'glimpse',
    'globe',
    'gloom',
    'glory',
    'glove',
    'glow',
    'glue',
    'goat',
    'goddess',
    'gold',
    'good',
    'goose',
    'gorilla',
    'gospel',
    'gossip',
    'govern',
    'gown',
    'grab',
    'grace',
    'grain',
    'grant',
    'grape',
    'grass',
    'gravity',
    'great',
    'green',
    'grid',
    'grief',
    'grit',
    'grocery',
    'group',
    'grow',
    'grunt',
    'guard',
    'guess',
    'guide',
    'guilt',
    'guitar',
    'gun',
    'gym',
    'habit',
    'hair',
    'half',
    'hammer',
    'hamster',
    'hand',
    'happy',
    'harbor',
    'hard',
    'harsh',
    'harvest',
    'hat',
    'have',
    'hawk',
    'hazard',
    'head',
    'health',
    'heart',
    'heavy',
    'hedgehog',
    'height',
    'hello',
    'helmet',
    'help',
    'hen',
    'hero',
    'hidden',
    'high',
    'hill',
    'hint',
    'hip',
    'hire',
    'history',
    'hobby',
    'hockey',
    'hold',
    'hole',
    'holiday',
    'hollow',
    'home',
    'honey',
    'hood',
    'hope',
    'horn',
    'horror',
    'horse',
    'hospital',
    'host',
    'hotel',
    'hour',
    'hover',
    'hub',
    'huge',
    'human',
    'humble',
    'humor',
    'hundred',
    'hungry',
    'hunt',
    'hurdle',
    'hurry',
    'hurt',
    'husband',
    'hybrid',
    'ice',
    'icon',
    'idea',
    'identify',
    'idle',
    'ignore',
    'ill',
    'illegal',
    'illness',
    'image',
    'imitate',
    'immense',
    'immune',
    'impact',
    'impose',
    'improve',
    'impulse',
    'inch',
    'include',
    'income',
    'increase',
    'index',
    'indicate',
    'indoor',
    'industry',
    'infant',
    'inflict',
    'inform',
    'inhale',
    'inherit',
    'initial',
    'inject',
    'injury',
    'inmate',
    'inner',
    'innocent',
    'input',
    'inquiry',
    'insane',
    'insect',
    'inside',
    'inspire',
    'install',
    'intact',
    'interest',
    'into',
    'invest',
    'invite',
    'involve',
    'iron',
    'island',
    'isolate',
    'issue',
    'item',
    'ivory',
    'jacket',
    'jaguar',
    'jar',
    'jazz',
    'jealous',
    'jeans',
    'jelly',
    'jewel',
    'job',
    'join',
    'joke',
    'journey',
    'joy',
    'judge',
    'juice',
    'jump',
    'jungle',
    'junior',
    'junk',
    'just',
    'kangaroo',
    'keen',
    'keep',
    'ketchup',
    'key',
    'kick',
    'kid',
    'kidney',
    'kind',
    'kingdom',
    'kiss',
    'kit',
    'kitchen',
    'kite',
    'kitten',
    'kiwi',
    'knee',
    'knife',
    'knock',
    'know',
    'lab',
    'label',
    'labor',
    'ladder',
    'lady',
    'lake',
    'lamp',
    'language',
    'laptop',
    'large',
    'later',
    'latin',
    'laugh',
    'laundry',
    'lava',
    'law',
    'lawn',
    'lawsuit',
    'layer',
    'lazy',
    'leader',
    'leaf',
    'learn',
    'leave',
    'lecture',
    'left',
    'leg',
    'legal',
    'legend',
    'leisure',
    'lemon',
    'lend',
    'length',
    'lens',
    'leopard',
    'lesson',
    'letter',
    'level',
    'liar',
    'liberty',
    'library',
    'license',
    'life',
    'lift',
    'light',
    'like',
    'limb',
    'limit',
    'link',
    'lion',
    'liquid',
    'list',
    'little',
    'live',
    'lizard',
    'load',
    'loan',
    'lobster',
    'local',
    'lock',
    'logic',
    'lonely',
    'long',
    'loop',
    'lottery',
    'loud',
    'lounge',
    'love',
    'loyal',
    'lucky',
    'luggage',
    'lumber',
    'lunar',
    'lunch',
    'luxury',
    'lyrics',
    'machine',
    'mad',
    'magic',
    'magnet',
    'maid',
    'mail',
    'main',
    'major',
    'make',
    'mammal',
    'man',
    'manage',
    'mandate',
    'mango',
    'mansion',
    'manual',
    'maple',
    'marble',
    'march',
    'margin',
    'marine',
    'market',
    'marriage',
    'mask',
    'mass',
    'master',
    'match',
    'material',
    'math',
    'matrix',
    'matter',
    'maximum',
    'maze',
    'meadow',
    'mean',
    'measure',
    'meat',
    'mechanic',
    'medal',
    'media',
    'melody',
    'melt',
    'member',
    'memory',
    'mention',
    'menu',
    'mercy',
    'merge',
    'merit',
    'merry',
    'mesh',
    'message',
    'metal',
    'method',
    'middle',
    'midnight',
    'milk',
    'million',
    'mimic',
    'mind',
    'minimum',
    'minor',
    'minute',
    'miracle',
    'mirror',
    'misery',
    'miss',
    'mistake',
    'mix',
    'mixed',
    'mixture',
    'mobile',
    'model',
    'modify',
    'mom',
    'moment',
    'monitor',
    'monkey',
    'monster',
    'month',
    'moon',
    'moral',
    'more',
    'morning',
    'mosquito',
    'mother',
    'motion',
    'motor',
    'mountain',
    'mouse',
    'move',
    'movie',
    'much',
    'muffin',
    'mule',
    'multiply',
    'muscle',
    'museum',
    'mushroom',
    'music',
    'must',
    'mutual',
    'myself',
    'mystery',
    'myth',
    'naive',
    'name',
    'napkin',
    'narrow',
    'nasty',
    'nation',
    'nature',
    'near',
    'neck',
    'need',
    'negative',
    'neglect',
    'neither',
    'nephew',
    'nerve',
    'nest',
    'net',
    'network',
    'neutral',
    'never',
    'news',
    'next',
    'nice',
    'night',
    'noble',
    'noise',
    'nominee',
    'noodle',
    'normal',
    'north',
    'nose',
    'notable',
    'note',
    'nothing',
    'notice',
    'novel',
    'now',
    'nuclear',
    'number',
    'nurse',
    'nut',
    'oak',
    'obey',
    'object',
    'oblige',
    'obscure',
    'observe',
    'obtain',
    'obvious',
    'occur',
    'ocean',
    'october',
    'odor',
    'off',
    'offer',
    'office',
    'often',
    'oil',
    'okay',
    'old',
    'olive',
    'olympic',
    'omit',
    'once',
    'one',
    'onion',
    'online',
    'only',
    'open',
    'opera',
    'opinion',
    'oppose',
    'option',
    'orange',
    'orbit',
    'orchard',
    'order',
    'ordinary',
    'organ',
    'orient',
    'original',
    'orphan',
    'ostrich',
    'other',
    'outdoor',
    'outer',
    'output',
    'outside',
    'oval',
    'oven',
    'over',
    'own',
    'owner',
    'oxygen',
    'oyster',
    'ozone',
    'pact',
    'paddle',
    'page',
    'pair',
    'palace',
    'palm',
    'panda',
    'panel',
    'panic',
    'panther',
    'paper',
    'parade',
    'parent',
    'park',
    'parrot',
    'party',
    'pass',
    'patch',
    'path',
    'patient',
    'patrol',
    'pattern',
    'pause',
    'pave',
    'payment',
    'peace',
    'peanut',
    'pear',
    'peasant',
    'pelican',
    'pen',
    'penalty',
    'pencil',
    'people',
    'pepper',
    'perfect',
    'permit',
    'person',
    'pet',
    'phone',
    'photo',
    'phrase',
    'physical',
    'piano',
    'picnic',
    'picture',
    'piece',
    'pig',
    'pigeon',
    'pill',
    'pilot',
    'pink',
    'pioneer',
    'pipe',
    'pistol',
    'pitch',
    'pizza',
    'place',
    'planet',
    'plastic',
    'plate',
    'play',
    'please',
    'pledge',
    'pluck',
    'plug',
    'plunge',
    'poem',
    'poet',
    'point',
    'polar',
    'pole',
    'police',
    'pond',
    'pony',
    'pool',
    'popular',
    'portion',
    'position',
    'possible',
    'post',
    'potato',
    'pottery',
    'poverty',
    'powder',
    'power',
    'practice',
    'praise',
    'predict',
    'prefer',
    'prepare',
    'present',
    'pretty',
    'prevent',
    'price',
    'pride',
    'primary',
    'print',
    'priority',
    'prison',
    'private',
    'prize',
    'problem',
    'process',
    'produce',
    'profit',
    'program',
    'project',
    'promote',
    'proof',
    'property',
    'prosper',
    'protect',
    'proud',
    'provide',
    'public',
    'pudding',
    'pull',
    'pulp',
    'pulse',
    'pumpkin',
    'punch',
    'pupil',
    'puppy',
    'purchase',
    'purity',
    'purpose',
    'purse',
    'push',
    'put',
    'puzzle',
    'pyramid',
    'quality',
    'quantum',
    'quarter',
    'question',
    'quick',
    'quit',
    'quiz',
    'quote',
    'rabbit',
    'raccoon',
    'race',
    'rack',
    'radar',
    'radio',
    'rail',
    'rain',
    'raise',
    'rally',
    'ramp',
    'ranch',
    'random',
    'range',
    'rapid',
    'rare',
    'rate',
    'rather',
    'raven',
    'raw',
    'razor',
    'ready',
    'real',
    'reason',
    'rebel',
    'rebuild',
    'recall',
    'receive',
    'recipe',
    'record',
    'recycle',
    'reduce',
    'reflect',
    'reform',
    'refuse',
    'region',
    'regret',
    'regular',
    'reject',
    'relax',
    'release',
    'relief',
    'rely',
    'remain',
    'remember',
    'remind',
    'remove',
    'render',
    'renew',
    'rent',
    'reopen',
    'repair',
    'repeat',
    'replace',
    'report',
    'require',
    'rescue',
    'resemble',
    'resist',
    'resource',
    'response',
    'result',
    'retire',
    'retreat',
    'return',
    'reunion',
    'reveal',
    'review',
    'reward',
    'rhythm',
    'rib',
    'ribbon',
    'rice',
    'rich',
    'ride',
    'ridge',
    'rifle',
    'right',
    'rigid',
    'ring',
    'riot',
    'ripple',
    'risk',
    'ritual',
    'rival',
    'river',
    'road',
    'roast',
    'robot',
    'robust',
    'rocket',
    'romance',
    'roof',
    'rookie',
    'room',
    'rose',
    'rotate',
    'rough',
    'round',
    'route',
    'royal',
    'rubber',
    'rude',
    'rug',
    'rule',
    'run',
    'runway',
    'rural',
    'sad',
    'saddle',
    'sadness',
    'safe',
    'sail',
    'salad',
    'salmon',
    'salon',
    'salt',
    'salute',
    'same',
    'sample',
    'sand',
    'satisfy',
    'satoshi',
    'sauce',
    'sausage',
    'save',
    'say',
    'scale',
    'scan',
    'scare',
    'scatter',
    'scene',
    'scheme',
    'school',
    'science',
    'scissors',
    'scorpion',
    'scout',
    'scrap',
    'screen',
    'script',
    'scrub',
    'sea',
    'search',
    'season',
    'seat',
    'second',
    'secret',
    'section',
    'security',
    'seed',
    'seek',
    'segment',
    'select',
    'sell',
    'seminar',
    'senior',
    'sense',
    'sentence',
    'series',
    'service',
    'session',
    'settle',
    'setup',
    'seven',
    'shadow',
    'shaft',
    'shallow',
    'share',
    'shed',
    'shell',
    'sheriff',
    'shield',
    'shift',
    'shine',
    'ship',
    'shiver',
    'shock',
    'shoe',
    'shoot',
    'shop',
    'short',
    'shoulder',
    'shove',
    'shrimp',
    'shrug',
    'shuffle',
    'shy',
    'sibling',
    'sick',
    'side',
    'siege',
    'sight',
    'sign',
    'silent',
    'silk',
    'silly',
    'silver',
    'similar',
    'simple',
    'since',
    'sing',
    'siren',
    'sister',
    'situate',
    'six',
    'size',
    'skate',
    'sketch',
    'ski',
    'skill',
    'skin',
    'skirt',
    'skull',
    'slab',
    'slam',
    'sleep',
    'slender',
    'slice',
    'slide',
    'slight',
    'slim',
    'slogan',
    'slot',
    'slow',
    'slush',
    'small',
    'smart',
    'smile',
    'smoke',
    'smooth',
    'snack',
    'snake',
    'snap',
    'sniff',
    'snow',
    'soap',
    'soccer',
    'social',
    'sock',
    'soda',
    'soft',
    'solar',
    'soldier',
    'solid',
    'solution',
    'solve',
    'someone',
    'song',
    'soon',
    'sorry',
    'sort',
    'soul',
    'sound',
    'soup',
    'source',
    'south',
    'space',
    'spare',
    'spatial',
    'spawn',
    'speak',
    'special',
    'speed',
    'spell',
    'spend',
    'sphere',
    'spice',
    'spider',
    'spike',
    'spin',
    'spirit',
    'split',
    'spoil',
    'sponsor',
    'spoon',
    'sport',
    'spot',
    'spray',
    'spread',
    'spring',
    'spy',
    'square',
    'squeeze',
    'squirrel',
    'stable',
    'stadium',
    'staff',
    'stage',
    'stairs',
    'stamp',
    'stand',
    'start',
    'state',
    'stay',
    'steak',
    'steel',
    'stem',
    'step',
    'stereo',
    'stick',
    'still',
    'sting',
    'stock',
    'stomach',
    'stone',
    'stool',
    'story',
    'stove',
    'strategy',
    'street',
    'strike',
    'strong',
    'struggle',
    'student',
    'stuff',
    'stumble',
    'style',
    'subject',
    'submit',
    'subway',
    'success',
    'such',
    'sudden',
    'suffer',
    'sugar',
    'suggest',
    'suit',
    'summer',
    'sun',
    'sunny',
    'sunset',
    'super',
    'supply',
    'supreme',
    'sure',
    'surface',
    'surge',
    'surprise',
    'surround',
    'survey',
    'suspect',
    'sustain',
    'swallow',
    'swamp',
    'swap',
    'swarm',
    'swear',
    'sweet',
    'swift',
    'swim',
    'swing',
    'switch',
    'sword',
    'symbol',
    'symptom',
    'syrup',
    'system',
    'table',
    'tackle',
    'tag',
    'tail',
    'talent',
    'talk',
    'tank',
    'tape',
    'target',
    'task',
    'taste',
    'tattoo',
    'taxi',
    'teach',
    'team',
    'tell',
    'ten',
    'tenant',
    'tennis',
    'tent',
    'term',
    'test',
    'text',
    'thank',
    'that',
    'theme',
    'then',
    'theory',
    'there',
    'they',
    'thing',
    'this',
    'thought',
    'three',
    'thrive',
    'throw',
    'thumb',
    'thunder',
    'ticket',
    'tide',
    'tiger',
    'tilt',
    'timber',
    'time',
    'tiny',
    'tip',
    'tired',
    'tissue',
    'title',
    'toast',
    'tobacco',
    'today',
    'toddler',
    'toe',
    'together',
    'toilet',
    'token',
    'tomato',
    'tomorrow',
    'tone',
    'tongue',
    'tonight',
    'tool',
    'tooth',
    'top',
    'topic',
    'topple',
    'torch',
    'tornado',
    'tortoise',
    'toss',
    'total',
    'tourist',
    'toward',
    'tower',
    'town',
    'toy',
    'track',
    'trade',
    'traffic',
    'tragic',
    'train',
    'transfer',
    'trap',
    'trash',
    'travel',
    'tray',
    'treat',
    'tree',
    'trend',
    'trial',
    'tribe',
    'trick',
    'trigger',
    'trim',
    'trip',
    'trophy',
    'trouble',
    'truck',
    'true',
    'truly',
    'trumpet',
    'trust',
    'truth',
    'try',
    'tube',
    'tuition',
    'tumble',
    'tuna',
    'tunnel',
    'turkey',
    'turn',
    'turtle',
    'twelve',
    'twenty',
    'twice',
    'twin',
    'twist',
    'two',
    'type',
    'typical',
    'ugly',
    'umbrella',
    'unable',
    'unaware',
    'uncle',
    'uncover',
    'under',
    'undo',
    'unfair',
    'unfold',
    'unhappy',
    'uniform',
    'unique',
    'unit',
    'universe',
    'unknown',
    'unlock',
    'until',
    'unusual',
    'unveil',
    'update',
    'upgrade',
    'uphold',
    'upon',
    'upper',
    'upset',
    'urban',
    'urge',
    'usage',
    'use',
    'used',
    'useful',
    'useless',
    'usual',
    'utility',
    'vacant',
    'vacuum',
    'vague',
    'valid',
    'valley',
    'valve',
    'van',
    'vanish',
    'vapor',
    'various',
    'vast',
    'vault',
    'vehicle',
    'velvet',
    'vendor',
    'venture',
    'venue',
    'verb',
    'verify',
    'version',
    'very',
    'vessel',
    'veteran',
    'viable',
    'vibrant',
    'vicious',
    'victory',
    'video',
    'view',
    'village',
    'vintage',
    'violin',
    'virtual',
    'virus',
    'visa',
    'visit',
    'visual',
    'vital',
    'vivid',
    'vocal',
    'voice',
    'void',
    'volcano',
    'volume',
    'vote',
    'voyage',
    'wage',
    'wagon',
    'wait',
    'walk',
    'wall',
    'walnut',
    'want',
    'warfare',
    'warm',
    'warrior',
    'wash',
    'wasp',
    'waste',
    'water',
    'wave',
    'way',
    'wealth',
    'weapon',
    'wear',
    'weasel',
    'weather',
    'web',
    'wedding',
    'weekend',
    'weird',
    'welcome',
    'west',
    'wet',
    'whale',
    'what',
    'wheat',
    'wheel',
    'when',
    'where',
    'whip',
    'whisper',
    'wide',
    'width',
    'wife',
    'wild',
    'will',
    'win',
    'window',
    'wine',
    'wing',
    'wink',
    'winner',
    'winter',
    'wire',
    'wisdom',
    'wise',
    'wish',
    'witness',
    'wolf',
    'woman',
    'wonder',
    'wood',
    'wool',
    'word',
    'work',
    'world',
    'worry',
    'worth',
    'wrap',
    'wreck',
    'wrestle',
    'wrist',
    'write',
    'wrong',
    'yard',
    'year',
    'yellow',
    'you',
    'young',
    'youth',
    'zebra',
    'zero',
    'zone',
    'zoo',
]
BIP39_WORD_INDEX = {w: i for i, w in enumerate(BIP39_WORDS)}


                         
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

HARDENED = 0x80000000

BTC_MAINNET = {
    "p2pkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh-p2sh": {"xprv": 0x049D7878, "xpub": 0x049D7CB2},
    "p2wpkh": {"xprv": 0x04B2430C, "xpub": 0x04B24746},
    "p2tr": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "wif": 0x80,
    "p2pkh_prefix": 0x00,
    "p2sh_prefix": 0x05,
    "hrp": "bc",
}

BTC_TESTNET = {
    "p2pkh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2wpkh-p2sh": {"xprv": 0x044A4E28, "xpub": 0x044A5262},
    "p2wpkh": {"xprv": 0x045F18BC, "xpub": 0x045F1CF6},
    "p2tr": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "wif": 0xEF,
    "p2pkh_prefix": 0x6F,
    "p2sh_prefix": 0xC4,
    "hrp": "tb",
}

BCH_TESTNET = {
    "p2pkh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2wpkh-p2sh": None,
    "p2wpkh": None,
    "p2tr": None,
    "wif": 0xEF,
    "p2pkh_prefix": 0x6F,
    "p2sh_prefix": 0xC4,
    "cashaddr_prefix": "bchtest",
}

LTC_MAINNET = {
                                                       
    "p2pkh": {"xprv": 0x019D9CFE, "xpub": 0x019DA462},
    "p2wpkh-p2sh": {"xprv": 0x01B26792, "xpub": 0x01B26EF6},
                                                                               
    "p2wpkh": {"xprv": 0x04B2430C, "xpub": 0x04B24746},
    "p2tr": {"xprv": 0x019D9CFE, "xpub": 0x019DA462},
    "wif": 0xB0,
    "p2pkh_prefix": 0x30,
    "p2sh_prefix": 0x32,
    "hrp": "ltc",
}

LTC_TESTNET = {
    "p2pkh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2wpkh-p2sh": {"xprv": 0x044A4E28, "xpub": 0x044A5262},
    "p2wpkh": {"xprv": 0x045F18BC, "xpub": 0x045F1CF6},
    "p2tr": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "wif": 0xEF,
    "p2pkh_prefix": 0x6F,
    "p2sh_prefix": 0x3A,
    "hrp": "tltc",
}

DOGE_MAINNET = {
                                                       
    "p2pkh": {"xprv": 0x02FAC398, "xpub": 0x02FACAFD},
                                                                   
                                                                       
    "p2wpkh-p2sh": {"xprv": 0x02FAC398, "xpub": 0x02FACAFD},
    "p2wpkh": {"xprv": 0x02FAC398, "xpub": 0x02FACAFD},
    "p2tr": None,
    "wif": 0x9E,
    "p2pkh_prefix": 0x1E,
    "p2sh_prefix": 0x16,
    "hrp": "doge",
}

DOGE_TESTNET = {
    "p2pkh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2wpkh-p2sh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2wpkh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2tr": None,
    "wif": 0xF1,
    "p2pkh_prefix": 0x71,
    "p2sh_prefix": 0xC4,
    "hrp": "tdge",
}

BCH_MAINNET = {
    "p2pkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh-p2sh": None,
    "p2wpkh": None,
    "p2tr": None,
    "wif": 0x80,
    "p2pkh_prefix": 0x00,
    "p2sh_prefix": 0x05,
    "cashaddr_prefix": "bitcoincash",
}

ETH_MAINNET = {
    "p2pkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh-p2sh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2tr": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "wif": None,
    "address_family": "ethereum",
}

def evm_network(label: str, note_key: str) -> dict:
    return {
        "p2pkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
        "p2wpkh-p2sh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
        "p2wpkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
        "p2tr": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
        "wif": None,
        "address_family": "evm",
        "evm_label": label,
        "evm_note_key": note_key,
    }


ETH_TESTNET = {**ETH_MAINNET}
BNB_MAINNET = evm_network("BNB Chain", "bnb_chain_note")
BNB_TESTNET = evm_network("BNB Chain Testnet", "bnb_chain_note")
AVALANCHE_MAINNET = evm_network("Avalanche C-Chain", "avalanche_c_chain_note")
AVALANCHE_TESTNET = evm_network("Avalanche Fuji C-Chain", "avalanche_c_chain_note")
POLYGON_MAINNET = evm_network("Polygon PoS", "polygon_note")
POLYGON_TESTNET = evm_network("Polygon Amoy Testnet", "polygon_note")

TRON_MAINNET = evm_network("TRON", "tron_note")
TRON_MAINNET["address_family"] = "tron"
TRON_TESTNET = {**TRON_MAINNET}

COSMOS_MAINNET = evm_network("Cosmos Hub", "cosmos_note")
COSMOS_MAINNET.update({"address_family": "cosmos", "address_hrp": "cosmos"})
COSMOS_TESTNET = {**COSMOS_MAINNET}

XRP_MAINNET = {
    "p2pkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh-p2sh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2tr": None,
    "wif": None,
    "address_family": "xrp",
}

SOLANA_MAINNET = {"address_family": "solana"}
SOLANA_TESTNET = {"address_family": "solana"}
STELLAR_MAINNET = {"address_family": "stellar"}
STELLAR_TESTNET = {"address_family": "stellar"}
CARDANO_MAINNET = {"address_family": "cardano", "address_hrp": "addr", "network_id": 1}
CARDANO_TESTNET = {"address_family": "cardano", "address_hrp": "addr_test", "network_id": 0}
XRP_TESTNET = {**XRP_MAINNET}

COINS = {
    "bitcoin": {"coin_type": 0, "mainnet": BTC_MAINNET, "testnet": BTC_TESTNET},
    "bitcoincash": {"coin_type": 0, "mainnet": BCH_MAINNET, "testnet": BCH_TESTNET},
    "litecoin": {"coin_type": 2, "mainnet": LTC_MAINNET, "testnet": LTC_TESTNET},
    "dogecoin": {"coin_type": 3, "mainnet": DOGE_MAINNET, "testnet": DOGE_TESTNET},
    "ethereum": {"coin_type": 60, "mainnet": ETH_MAINNET, "testnet": ETH_TESTNET},
    "bnbchain": {"coin_type": 60, "mainnet": BNB_MAINNET, "testnet": BNB_TESTNET},
    "avalanche": {"coin_type": 60, "mainnet": AVALANCHE_MAINNET, "testnet": AVALANCHE_TESTNET},
    "polygon": {"coin_type": 60, "mainnet": POLYGON_MAINNET, "testnet": POLYGON_TESTNET},
    "tron": {"coin_type": 195, "mainnet": TRON_MAINNET, "testnet": TRON_TESTNET},
    "cosmos": {"coin_type": 118, "mainnet": COSMOS_MAINNET, "testnet": COSMOS_TESTNET},
    "solana": {"coin_type": 501, "mainnet": SOLANA_MAINNET, "testnet": SOLANA_TESTNET},
    "stellar": {"coin_type": 148, "mainnet": STELLAR_MAINNET, "testnet": STELLAR_TESTNET},
    "cardano": {"coin_type": 1815, "mainnet": CARDANO_MAINNET, "testnet": CARDANO_TESTNET},
    "xrp": {"coin_type": 144, "mainnet": XRP_MAINNET, "testnet": XRP_TESTNET},
}

DEFAULT_ACCOUNT_DERIVATION = {
    "bitcoin": "m/0'",
    "bitcoincash": "m/0'",
    "litecoin": "m/84'/2'/0'",
    "dogecoin": "m/44'/3'/0'",
    "ethereum": "m/44'/60'/0'",
    "bnbchain": "m/44'/60'/0'",
    "avalanche": "m/44'/60'/0'",
    "polygon": "m/44'/60'/0'",
    "tron": "m/44'/195'/0'",
    "cosmos": "m/44'/118'/0'",
    "solana": "m/44'/501'/0'",
    "stellar": "m/44'/148'/0'",
    "cardano": "m/1852'/1815'/0'/0/0",
    "xrp": "m/44'/144'/0'",
}

TESTNET_UTXO_DERIVATION = {
    "p2pkh": "m/44'/1'/0'",
    "p2wpkh-p2sh": "m/49'/1'/0'",
    "p2wpkh": "m/84'/1'/0'",
    "p2tr": "m/86'/1'/0'",
}

B58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
XRP_B58_ALPHABET = b"rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz"
BECH32_ALPHABET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def keccak256(data: bytes) -> bytes:
                                                                        
    mask = (1 << 64) - 1
    rate = 136
    rot = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14],
    ]
    rc = [
        0x0000000000000001,
        0x0000000000008082,
        0x800000000000808A,
        0x8000000080008000,
        0x000000000000808B,
        0x0000000080000001,
        0x8000000080008081,
        0x8000000000008009,
        0x000000000000008A,
        0x0000000000000088,
        0x0000000080008009,
        0x000000008000000A,
        0x000000008000808B,
        0x800000000000008B,
        0x8000000000008089,
        0x8000000000008003,
        0x8000000000008002,
        0x8000000000000080,
        0x000000000000800A,
        0x800000008000000A,
        0x8000000080008081,
        0x8000000000008080,
        0x0000000080000001,
        0x8000000080008008,
    ]

    def rol(x: int, n: int) -> int:
        return ((x << n) | (x >> (64 - n))) & mask if n else x & mask

    def permute(state: List[int]) -> None:
        for rnd in range(24):
            c = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
            d = [c[(x - 1) % 5] ^ rol(c[(x + 1) % 5], 1) for x in range(5)]
            for x in range(5):
                for y in range(5):
                    state[x + 5 * y] = (state[x + 5 * y] ^ d[x]) & mask
            b = [0] * 25
            for x in range(5):
                for y in range(5):
                    b[y + 5 * ((2 * x + 3 * y) % 5)] = rol(state[x + 5 * y], rot[x][y])
            for x in range(5):
                for y in range(5):
                    state[x + 5 * y] = (b[x + 5 * y] ^ ((~b[((x + 1) % 5) + 5 * y]) & b[((x + 2) % 5) + 5 * y])) & mask
            state[0] = (state[0] ^ rc[rnd]) & mask

    state = [0] * 25
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % rate != rate - 1:
        padded.append(0)
    padded.append(0x80)
    for offset in range(0, len(padded), rate):
        block = padded[offset : offset + rate]
        for i in range(rate // 8):
            state[i] ^= int.from_bytes(block[i * 8 : i * 8 + 8], "little")
        permute(state)
    return b"".join(x.to_bytes(8, "little") for x in state)[:32]


def hash160(b: bytes) -> bytes:
    h = hashlib.new("ripemd160")
    h.update(hashlib.sha256(b).digest())
    return h.digest()


def hmac_sha512(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha512).digest()


def b58encode(raw: bytes, alphabet: bytes = B58_ALPHABET) -> str:
    n = int.from_bytes(raw, "big")
    out = bytearray()
    while n > 0:
        n, r = divmod(n, 58)
        out.append(alphabet[r])
    out.reverse()
    pad = 0
    for c in raw:
        if c == 0:
            pad += 1
        else:
            break
    return (alphabet[0:1] * pad + out).decode("ascii")


def b58check(payload: bytes, alphabet: bytes = B58_ALPHABET) -> str:
    checksum = sha256(sha256(payload))[:4]
    return b58encode(payload + checksum, alphabet)


def bech32_polymod(values: List[int]) -> int:
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ v
        for i in range(5):
            if (top >> i) & 1:
                chk ^= gen[i]
    return chk


def bech32_hrp_expand(hrp: str) -> List[int]:
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_create_checksum(hrp: str, data: List[int]) -> List[int]:
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> (5 * (5 - i))) & 31 for i in range(6)]


def bech32_encode(hrp: str, data: List[int]) -> str:
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join(BECH32_ALPHABET[d] for d in combined)


def bech32m_create_checksum(hrp: str, data: List[int]) -> List[int]:
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 0x2BC830A3
    return [(polymod >> (5 * (5 - i))) & 31 for i in range(6)]


def bech32m_encode(hrp: str, data: List[int]) -> str:
    combined = data + bech32m_create_checksum(hrp, data)
    return hrp + "1" + "".join(BECH32_ALPHABET[d] for d in combined)


def convertbits(data: bytes, frombits: int, tobits: int, pad: bool = True) -> List[int]:
    acc = 0
    bits = 0
    out = []
    maxv = (1 << tobits) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            raise ValueError("invalid bits")
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            out.append((acc >> bits) & maxv)
    if pad:
        if bits:
            out.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise ValueError("invalid bits")
    return out


def segwit_addr_v0(hrp: str, witprog: bytes) -> str:
    return bech32_encode(hrp, [0] + convertbits(witprog, 8, 5))


def segwit_addr_v1(hrp: str, witprog: bytes) -> str:
    return bech32m_encode(hrp, [1] + convertbits(witprog, 8, 5))


def cashaddr_polymod(values: List[int]) -> int:
    gen = [0x98F2BC8E61, 0x79B76D99E2, 0xF33E5FB3C4, 0xAE2EABE2A8, 0x1E4F43E470]
    chk = 1
    for value in values:
        top = chk >> 35
        chk = ((chk & 0x07FFFFFFFF) << 5) ^ value
        for i, g in enumerate(gen):
            if (top >> i) & 1:
                chk ^= g
    return chk ^ 1


def cashaddr_prefix_expand(prefix: str) -> List[int]:
    return [ord(c) & 31 for c in prefix.lower()] + [0]


def cashaddr_encode(prefix: str, type_value: int, payload_hash: bytes) -> str:
    if len(payload_hash) != 20:
        raise ValueError("unsupported Bitcoin Cash hash length")
    version = (type_value << 3) | 0
    payload = convertbits(bytes([version]) + payload_hash, 8, 5, True)
    values = cashaddr_prefix_expand(prefix) + payload + [0] * 8
    checksum_value = cashaddr_polymod(values)
    checksum = [(checksum_value >> (5 * (7 - i))) & 31 for i in range(8)]
    return prefix.lower() + ":" + "".join(BECH32_ALPHABET[v] for v in payload + checksum)


ED25519_P = (1 << 255) - 19
ED25519_D = (-121665 * pow(121666, -1, ED25519_P)) % ED25519_P
ED25519_G = (
    15112221349535400772501151409588531511454012693041857206046113283949847762202,
    46316835694926478169428394003475163141307993866256225615783033603165251855960,
)
ED25519_L = (1 << 252) + 27742317777372353535851937790883648493


def le_bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, "little")


def int_to_le_bytes(value: int, length: int) -> bytes:
    return int(value).to_bytes(length, "little")


def ed25519_point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    xy = (ED25519_D * x1 * x2 * y1 * y2) % ED25519_P
    x3 = ((x1 * y2 + y1 * x2) * pow((1 + xy) % ED25519_P, -1, ED25519_P)) % ED25519_P
    y3 = ((y1 * y2 + x1 * x2) * pow((1 - xy) % ED25519_P, -1, ED25519_P)) % ED25519_P
    return (x3, y3)


def ed25519_point_mul(k: int, point=ED25519_G):
    n = int(k)
    result = (0, 1)
    addend = point
    while n > 0:
        if n & 1:
            result = ed25519_point_add(result, addend)
        addend = ed25519_point_add(addend, addend)
        n >>= 1
    return result


def ed25519_public_key_from_seed(seed: bytes) -> bytes:
    digest = hashlib.sha512(seed).digest()
    scalar = bytearray(digest[:32])
    scalar[0] &= 248
    scalar[31] &= 127
    scalar[31] |= 64
    point = ed25519_point_mul(le_bytes_to_int(bytes(scalar)))
    encoded = bytearray(int_to_le_bytes(point[1], 32))
    encoded[31] = (encoded[31] & 0x7F) | ((point[0] & 1) << 7)
    return bytes(encoded)


def ed25519_public_key_from_scalar_bytes(scalar_bytes: bytes) -> bytes:
    point = ed25519_point_mul(le_bytes_to_int(scalar_bytes))
    encoded = bytearray(int_to_le_bytes(point[1], 32))
    encoded[31] = (encoded[31] & 0x7F) | ((point[0] & 1) << 7)
    return bytes(encoded)


def reduce_ed25519_scalar(data: bytes) -> bytes:
    scalar = le_bytes_to_int(data) % ED25519_L
    if scalar == 0:
        scalar = 1
    return int_to_le_bytes(scalar, 32)


def master_from_seed_ed25519(seed: bytes) -> Dict[str, bytes]:
    digest = hmac_sha512(b"ed25519 seed", seed)
    return {"k": digest[:32], "c": digest[32:]}


def ckd_priv_ed25519(node: Dict[str, bytes], index: int) -> Dict[str, bytes]:
    if not (index & HARDENED):
        raise ValueError("Ed25519 derivation requires hardened path indexes")
    digest = hmac_sha512(node["c"], b"\x00" + node["k"] + ser32(index))
    return {"k": digest[:32], "c": digest[32:]}


def derive_ed25519(node: Dict[str, bytes], path: str) -> Dict[str, bytes]:
    cur = node
    for index in parse_path(path):
        cur = ckd_priv_ed25519(cur, index)
    return cur


def path_from_indexes(indexes: List[int]) -> str:
    if not indexes:
        return "m"
    return "m/" + "/".join(f"{i - HARDENED}'" if (i & HARDENED) else str(i) for i in indexes)


def solana_path_for_index(base_path: str, index: int) -> str:
    ints = parse_path(base_path)
    if (
        len(ints) >= 4
        and (ints[0] & 0x7FFFFFFF) == 44
        and (ints[1] & 0x7FFFFFFF) == 501
        and (ints[-1] & 0x7FFFFFFF) == 0
    ):
        next_path = list(ints)
        next_path[2] = (index | HARDENED) & 0xFFFFFFFF
        return path_from_indexes(next_path)
    return normalize_path(base_path) if index == 0 else normalize_path(base_path) + f"/{index}'"


def account_path_for_index(base_path: str, coin_type: int, index: int) -> str:
    ints = parse_path(base_path)
    if len(ints) >= 3 and (ints[0] & 0x7FFFFFFF) == 44 and (ints[1] & 0x7FFFFFFF) == coin_type:
        next_path = list(ints)
        next_path[2] = (index | HARDENED) & 0xFFFFFFFF
        return path_from_indexes(next_path)
    return normalize_path(base_path) if index == 0 else normalize_path(base_path) + f"/{index}'"


def monero_base58_encode(data: bytes) -> str:
    encoded_block_sizes = [0, 2, 3, 5, 6, 7, 9, 10, 11]
    out = []
    for offset in range(0, len(data), 8):
        block = data[offset : offset + 8]
        num = int.from_bytes(block, "big")
        enc = ""
        while num > 0:
            num, mod_value = divmod(num, 58)
            enc = chr(B58_ALPHABET[mod_value]) + enc
        out.append(enc.rjust(encoded_block_sizes[len(block)], chr(B58_ALPHABET[0])))
    return "".join(out)


def monero_address_from_spend_key(private_spend_key: bytes) -> Dict[str, bytes | str]:
    private_view_key = reduce_ed25519_scalar(keccak256(private_spend_key))
    public_spend_key = ed25519_public_key_from_scalar_bytes(private_spend_key)
    public_view_key = ed25519_public_key_from_scalar_bytes(private_view_key)
    body = b"\x12" + public_spend_key + public_view_key
    checksum = keccak256(body)[:4]
    return {
        "address": monero_base58_encode(body + checksum),
        "private_view_key": private_view_key,
        "public_spend_key": public_spend_key,
        "public_view_key": public_view_key,
    }


BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"


def base32_encode_no_padding(data: bytes) -> str:
    bits = 0
    value = 0
    out = []
    for byte in data:
        value = (value << 8) | byte
        bits += 8
        while bits >= 5:
            out.append(BASE32_ALPHABET[(value >> (bits - 5)) & 31])
            bits -= 5
    if bits:
        out.append(BASE32_ALPHABET[(value << (5 - bits)) & 31])
    return "".join(out)


def crc16_xmodem(data: bytes) -> bytes:
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if (crc & 0x8000) else (crc << 1)
            crc &= 0xFFFF
    return bytes([crc & 0xFF, (crc >> 8) & 0xFF])


def stellar_strkey(version_byte: int, payload: bytes) -> str:
    body = bytes([version_byte]) + payload
    return base32_encode_no_padding(body + crc16_xmodem(body))


def stellar_public_address(public_key: bytes) -> str:
    return stellar_strkey(6 << 3, public_key)


def stellar_secret_seed(private_seed: bytes) -> str:
    return stellar_strkey(18 << 3, private_seed)


def mnemonic_entropy_bytes(mnemonic: str) -> bytes:
    words = normalize_mnemonic_words(mnemonic)
    checksum_bits = len(words) // 3
    entropy_bits = len(words) * 11 - checksum_bits
    acc = 0
    for word in words:
        acc = (acc << 11) | BIP39_WORD_INDEX[word]
    entropy = acc >> checksum_bits
    return entropy.to_bytes(entropy_bits // 8, "big")


def cardano_icarus_master_from_entropy(entropy: bytes, passphrase: str = "") -> Dict[str, bytes]:
    password = normalize_nfkd(passphrase or "").encode("utf-8")
    key_bytes = bytearray(hashlib.pbkdf2_hmac("sha512", password, entropy, 4096, dklen=96))
    key_bytes[0] &= 0xF8
    key_bytes[31] &= 0x1F
    key_bytes[31] |= 0x40
    return {"k": bytes(key_bytes[:64]), "c": bytes(key_bytes[64:96])}


def ser32_le(index: int) -> bytes:
    return (index & 0xFFFFFFFF).to_bytes(4, "little")


def cardano_public_key_from_private(private_key: bytes) -> bytes:
    return ed25519_public_key_from_scalar_bytes(private_key[:32])


def ckd_priv_cardano(node: Dict[str, bytes], index: int) -> Dict[str, bytes]:
    idx = ser32_le(index)
    priv = node["k"]
    pub = cardano_public_key_from_private(priv)
    if index & HARDENED:
        z = hmac_sha512(node["c"], b"\x00" + priv + idx)
        c_digest = hmac_sha512(node["c"], b"\x01" + priv + idx)
    else:
        z = hmac_sha512(node["c"], b"\x02" + pub + idx)
        c_digest = hmac_sha512(node["c"], b"\x03" + pub + idx)
    kl = le_bytes_to_int(priv[:32])
    kr = le_bytes_to_int(priv[32:64])
    zl = le_bytes_to_int(z[:28])
    zr = le_bytes_to_int(z[32:64])
    child_left = kl + (8 * zl)
    if child_left % ED25519_L == 0:
        raise ValueError("invalid Cardano child key")
    child_right = (kr + zr) % (1 << 256)
    return {"k": int_to_le_bytes(child_left, 32) + int_to_le_bytes(child_right, 32), "c": c_digest[32:64]}


def derive_cardano(node: Dict[str, bytes], path: str) -> Dict[str, bytes]:
    cur = node
    for index in parse_path(path):
        cur = ckd_priv_cardano(cur, index)
    return cur


def cardano_paths_for_index(base_path: str, index: int) -> Dict[str, str]:
    ints = parse_path(base_path)
    account = HARDENED
    if len(ints) >= 3 and (ints[0] & 0x7FFFFFFF) == 1852 and (ints[1] & 0x7FFFFFFF) == 1815:
        account = ints[2]
    return {
        "payment_path": path_from_indexes([1852 | HARDENED, 1815 | HARDENED, account, 0, index]),
        "staking_path": path_from_indexes([1852 | HARDENED, 1815 | HARDENED, account, 2, 0]),
    }


def cardano_shelley_base_address(
    payment_public_key: bytes,
    staking_public_key: bytes,
    network_id: int = 1,
    hrp: str = "addr",
) -> str:
    payment_hash = hashlib.blake2b(payment_public_key, digest_size=28).digest()
    stake_hash = hashlib.blake2b(staking_public_key, digest_size=28).digest()
    raw = bytes([network_id & 0x0F]) + payment_hash + stake_hash
    return bech32_encode(hrp, convertbits(raw, 8, 5, True))


def inv_mod(a: int, n: int) -> int:
    return pow(a, -1, n)


def point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        lam = (3 * x1 * x1) * inv_mod(2 * y1 % P, P) % P
    else:
        lam = (y2 - y1) * inv_mod((x2 - x1) % P, P) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)


def point_mul(k: int, point=G):
    if k % N == 0 or point is None:
        return None
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


def ser32(i: int) -> bytes:
    return i.to_bytes(4, "big")


def ser256(i: int) -> bytes:
    return i.to_bytes(32, "big")


def ser_pubkey(p) -> bytes:
    x, y = p
    return (b"\x03" if (y & 1) else b"\x02") + x.to_bytes(32, "big")


def xonly_pubkey(p) -> bytes:
    x, _ = p
    return x.to_bytes(32, "big")


def negate_point(p):
    if p is None:
        return None
    x, y = p
    return (x, (-y) % P)


def tagged_hash(tag: str, msg: bytes) -> bytes:
    tag_hash = sha256(tag.encode("utf-8"))
    return sha256(tag_hash + tag_hash + msg)


def normalize_nfkd(s: str) -> str:
    return unicodedata.normalize("NFKD", s)


def normalize_mnemonic_words(mnemonic: str) -> List[str]:
    return normalize_nfkd(" ".join(mnemonic.strip().split())).split(" ")


def bip39_validate(mnemonic: str) -> Tuple[bool, bool, str]:
    words = normalize_mnemonic_words(mnemonic)
    wc = len(words)
    if wc not in (12, 24):
        return False, False, "Only 12-word and 24-word mnemonics are supported."
    if any(w not in BIP39_WORD_INDEX for w in words):
        return False, False, "Mnemonic contains unknown words outside the BIP39 English list."

    acc = 0
    for w in words:
        acc = (acc << 11) | BIP39_WORD_INDEX[w]

    checksum_bits = wc // 3
    entropy_bits = wc * 11 - checksum_bits
    entropy_int = acc >> checksum_bits
    checksum_int = acc & ((1 << checksum_bits) - 1)

    entropy = entropy_int.to_bytes(entropy_bits // 8, "big")
    hash_int = int.from_bytes(sha256(entropy), "big")
    expected_checksum = hash_int >> (256 - checksum_bits)
    checksum_ok = checksum_int == expected_checksum
    if not checksum_ok:
        return True, False, "Mnemonic words are valid BIP39 words, but checksum is invalid."
    return True, True, "Mnemonic is valid BIP39 (English word list + checksum)."


def generate_random_mnemonic(word_count: int) -> str:
    if word_count not in (12, 24):
        raise ValueError("Only 12-word and 24-word mnemonics are supported.")
    checksum_bits = word_count // 3
    entropy_bits = word_count * 11 - checksum_bits
    entropy = os.urandom(entropy_bits // 8)
    checksum = int.from_bytes(sha256(entropy), "big") >> (256 - checksum_bits)
    bits = (int.from_bytes(entropy, "big") << checksum_bits) | checksum
    words = [None] * word_count
    for i in range(word_count - 1, -1, -1):
        words[i] = BIP39_WORDS[bits & 0x7FF]
        bits >>= 11
    mnemonic = " ".join(words)
    words_ok, checksum_ok, _ = bip39_validate(mnemonic)
    if not (words_ok and checksum_ok):
        raise ValueError("Generated mnemonic failed validation.")
    return mnemonic


def detect_seed_format(word_count: int, words_ok: bool, checksum_ok: bool) -> Tuple[str, str]:
    if word_count in (12, 24) and words_ok and checksum_ok:
        return "HD wallet mnemonic", "BIP-39 mnemonic (English)"
    if word_count in (12, 24) and words_ok:
        return "Unrecognized or incomplete wallet seed", "BIP-39-like mnemonic (English words, checksum invalid)"
    return "Unknown", "Unknown or unsupported mnemonic format"


def analyze_mnemonic(mnemonic: str, passphrase: str = "") -> Dict:
    words = normalize_mnemonic_words(mnemonic)
    wc = len(words)
    details = {
        "word_count": wc,
        "wordlist_validity": "Invalid",
        "entropy_bits": None,
        "checksum_bits": None,
        "checksum_match": "Invalid",
        "bip39_compliance": "No",
        "bip39_seed_512_bit": None,
        "master_private_key": None,
        "master_chain_code": None,
        "root_fingerprint": None,
        "keystore_type": "Unknown",
        "seed_format_detection": "Unknown or unsupported mnemonic format",
        "passphrase_warning": None,
        "message": "",
    }
    if wc not in (12, 24):
        details["message"] = "Only 12-word and 24-word mnemonics are supported."
        return {"words_ok": False, "checksum_ok": False, **details}
    details["checksum_bits"] = wc // 3
    details["entropy_bits"] = wc * 11 - details["checksum_bits"]
    if any(w not in BIP39_WORD_INDEX for w in words):
        details["message"] = "Mnemonic contains unknown words outside the BIP39 English list."
        return {"words_ok": False, "checksum_ok": False, **details}

    details["wordlist_validity"] = "Valid"
    acc = 0
    for w in words:
        acc = (acc << 11) | BIP39_WORD_INDEX[w]
    checksum_bits = details["checksum_bits"]
    entropy_bits = details["entropy_bits"]
    entropy_int = acc >> checksum_bits
    checksum_int = acc & ((1 << checksum_bits) - 1)
    entropy = entropy_int.to_bytes(entropy_bits // 8, "big")
    hash_int = int.from_bytes(sha256(entropy), "big")
    expected_checksum = hash_int >> (256 - checksum_bits)
    checksum_ok = checksum_int == expected_checksum
    keystore_type, seed_format_detection = detect_seed_format(wc, True, checksum_ok)
    details["checksum_match"] = "Valid" if checksum_ok else "Invalid"
    details["bip39_compliance"] = "Yes" if checksum_ok else "No"
    details["keystore_type"] = keystore_type
    details["seed_format_detection"] = seed_format_detection
    details["passphrase_warning"] = "This seed may require a passphrase" if checksum_ok and not passphrase else None

    if not checksum_ok:
        details["message"] = "Mnemonic words are valid BIP39 words, but checksum is invalid."
        return {"words_ok": True, "checksum_ok": False, **details}

    seed = bip39_to_seed(mnemonic, passphrase)
    root = master_from_seed(seed)
    details["bip39_seed_512_bit"] = seed.hex()
    details["master_private_key"] = ser256(root.k).hex()
    details["master_chain_code"] = root.c.hex()
    details["root_fingerprint"] = hash160(ser_pubkey(root.pub()))[:4].hex()
    details["message"] = "Mnemonic is valid BIP39 (English word list + checksum)."
    return {"words_ok": True, "checksum_ok": True, **details}


def bip39_to_seed(mnemonic: str, passphrase: str) -> bytes:
    m = normalize_nfkd(" ".join(mnemonic.strip().split()))
    p = normalize_nfkd(passphrase)
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048, dklen=64)


def xor_stream_crypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < len(data):
        block = hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        out.extend(block)
        counter += 1
    return bytes(a ^ b for a, b in zip(data, out[: len(data)]))


ARC_MAGIC = "YELLOWSPHERE-ARC"
ARC_ARMOR_HEADER = "YELLOWSPHERE-ARC-V2"
ARC_V2_FORMAT = "yellowsphere-encrypted-seed-v2"
ARC_V2_KDF_ITERATIONS = 1000000
ARC_V2_MIN_KDF_ITERATIONS = 600000
ARC_V2_SALT_BYTES = 32
ARC_V2_NONCE_BYTES = 24


def b64encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64decode_required(value: object, field_name: str, expected_len: int | None = None) -> bytes:
    if not isinstance(value, str) or not value:
        raise ValueError(f"Encrypted seed file is missing {field_name}.")
    try:
        data = base64.b64decode(value, validate=True)
    except Exception as e:
        raise ValueError(f"Encrypted seed file has invalid {field_name}.") from e
    if expected_len is not None and len(data) != expected_len:
        raise ValueError(f"Encrypted seed file has invalid {field_name} length.")
    return data


def arc_v2_stream_crypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    pass
\
\
\
\
       
    out = bytearray()
    counter = 0
    while len(out) < len(data):
        msg = b"YellowSphere ARC v2 stream\x00" + nonce + counter.to_bytes(8, "big")
        out.extend(hmac.new(key, msg, hashlib.sha512).digest())
        counter += 1
    return bytes(a ^ b for a, b in zip(data, out[: len(data)]))


def arc_v2_keys(password: str, salt: bytes, iterations: int) -> Tuple[bytes, bytes]:
    if iterations < ARC_V2_MIN_KDF_ITERATIONS:
        raise ValueError("Encrypted seed file uses too few KDF iterations.")
    password_bytes = normalize_nfkd(password).encode("utf-8")
    master_key = hashlib.pbkdf2_hmac("sha512", password_bytes, salt, iterations, dklen=64)
    enc_key = hmac.new(master_key, b"YellowSphere ARC v2 encryption key", hashlib.sha512).digest()
    mac_key = hmac.new(master_key, b"YellowSphere ARC v2 authentication key", hashlib.sha512).digest()
    return enc_key, mac_key


def arc_v2_mac_data(bundle: Dict, salt: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    kdf = bundle.get("kdf", {})
    cipher = bundle.get("cipher", {})
    parts = [
        b"YellowSphere ARC v2 MAC",
        str(bundle.get("magic", "")).encode("utf-8"),
        str(bundle.get("format", "")).encode("utf-8"),
        str(bundle.get("version", "")).encode("utf-8"),
        str(bundle.get("created_at", "")).encode("utf-8"),
        str(kdf.get("name", "")).encode("utf-8"),
        str(kdf.get("hash", "")).encode("utf-8"),
        str(kdf.get("iterations", "")).encode("utf-8"),
        str(cipher.get("name", "")).encode("utf-8"),
        salt,
        nonce,
        ciphertext,
    ]
    return b"\x00".join(parts)


def normalize_decrypted_mnemonic(payload: Dict) -> str:
    if not isinstance(payload, dict):
        raise ValueError("Encrypted seed file contents are invalid.")
    mnemonic = " ".join(normalize_mnemonic_words(str(payload.get("mnemonic", ""))))
    if not mnemonic:
        raise ValueError("Encrypted seed file did not contain a mnemonic.")
    expected_count = payload.get("word_count")
    if expected_count is not None and int(expected_count) != len(normalize_mnemonic_words(mnemonic)):
        raise ValueError("Encrypted seed file word count does not match mnemonic.")
    return mnemonic


def encrypt_v2(mnemonic: str, password: str) -> Dict:
                                                                               
    words = normalize_mnemonic_words(mnemonic)
    if len(words) not in (12, 24):
        raise ValueError("Only 12-word and 24-word mnemonics can be encrypted.")
    salt = os.urandom(ARC_V2_SALT_BYTES)
    nonce = os.urandom(ARC_V2_NONCE_BYTES)
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    bundle = {
        "magic": ARC_MAGIC,
        "format": ARC_V2_FORMAT,
        "version": 2,
        "created_at": created_at,
        "kdf": {
            "name": "PBKDF2",
            "hash": "SHA-512",
            "iterations": ARC_V2_KDF_ITERATIONS,
            "salt_b64": b64encode_bytes(salt),
        },
        "cipher": {
            "name": "HMAC-SHA512-CTR",
            "nonce_b64": b64encode_bytes(nonce),
        },
    }
    payload = {
        "mnemonic": " ".join(words),
        "word_count": len(words),
        "created_at": created_at,
    }
    plaintext = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    enc_key, mac_key = arc_v2_keys(password, salt, ARC_V2_KDF_ITERATIONS)
    ciphertext = arc_v2_stream_crypt(plaintext, enc_key, nonce)
    bundle["ciphertext_b64"] = b64encode_bytes(ciphertext)
    mac = hmac.new(mac_key, arc_v2_mac_data(bundle, salt, nonce, ciphertext), hashlib.sha512).digest()
    bundle["mac_b64"] = b64encode_bytes(mac)
    return bundle


def decrypt_v2(bundle: Dict, password: str) -> str:
    if bundle.get("magic") != ARC_MAGIC or bundle.get("version") != 2 or bundle.get("format") != ARC_V2_FORMAT:
        raise ValueError("Unsupported encrypted seed file format.")
    kdf = bundle.get("kdf")
    cipher = bundle.get("cipher")
    if not isinstance(kdf, dict) or not isinstance(cipher, dict):
        raise ValueError("Encrypted seed file is malformed.")
    if kdf.get("name") != "PBKDF2" or kdf.get("hash") != "SHA-512":
        raise ValueError("Unsupported encrypted seed file KDF.")
    if cipher.get("name") != "HMAC-SHA512-CTR":
        raise ValueError("Unsupported encrypted seed file cipher.")
    try:
        iterations = int(kdf.get("iterations"))
    except Exception as e:
        raise ValueError("Encrypted seed file has invalid KDF iterations.") from e
    salt = b64decode_required(kdf.get("salt_b64"), "salt_b64", ARC_V2_SALT_BYTES)
    nonce = b64decode_required(cipher.get("nonce_b64"), "nonce_b64", ARC_V2_NONCE_BYTES)
    ciphertext = b64decode_required(bundle.get("ciphertext_b64"), "ciphertext_b64")
    expected_mac = b64decode_required(bundle.get("mac_b64"), "mac_b64", 64)
    enc_key, mac_key = arc_v2_keys(password, salt, iterations)
    actual_mac = hmac.new(mac_key, arc_v2_mac_data(bundle, salt, nonce, ciphertext), hashlib.sha512).digest()
    if not hmac.compare_digest(actual_mac, expected_mac):
        raise ValueError("Unable to decrypt seed file. The password may be incorrect or the file may be corrupted.")
    plaintext = arc_v2_stream_crypt(ciphertext, enc_key, nonce)
    try:
        payload = json.loads(plaintext.decode("utf-8"))
    except Exception as e:
        raise ValueError("Encrypted seed file contents are invalid.") from e
    return normalize_decrypted_mnemonic(payload)


def decrypt_v1(bundle: Dict, password: str) -> str:
    if bundle.get("format") not in ("yellowsphere-encrypted-seed-v2", "yellowsphere-encrypted-seed-python-v1"):
        raise ValueError("Unsupported encrypted seed file format.")
    try:
        iterations = int(bundle["kdf"]["iterations"])
        salt = base64.b64decode(bundle["kdf"]["salt_b64"])
        nonce = base64.b64decode(bundle["cipher"]["nonce_b64"])
        ciphertext = base64.b64decode(bundle["ciphertext_b64"])
        expected_mac = base64.b64decode(bundle["mac_b64"])
    except Exception as e:
        raise ValueError("Encrypted seed file is malformed.") from e
    password_bytes = normalize_nfkd(password).encode("utf-8")
    derived = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, iterations, dklen=64)
    enc_key, mac_key = derived[:32], derived[32:]
    actual_mac = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(actual_mac, expected_mac):
        raise ValueError("Unable to decrypt seed file. The password may be incorrect or the file may be corrupted.")
    plaintext = xor_stream_crypt(ciphertext, enc_key, nonce)
    try:
        payload = json.loads(plaintext.decode("utf-8"))
    except Exception as e:
        raise ValueError("Encrypted seed file contents are invalid.") from e
    return normalize_decrypted_mnemonic(payload)


def encrypt_seed_bundle(mnemonic: str, password: str) -> Dict:
    return encrypt_v2(mnemonic, password)


def decrypt_seed_bundle(bundle: Dict, password: str) -> str:
    return decrypt(bundle, password)


def serialize_seed_bundle(bundle: Dict) -> str:
    payload = json.dumps(bundle, separators=(",", ":"), sort_keys=True).encode("utf-8")
    encoded = base64.b64encode(payload).decode("ascii")
    return f"{ARC_ARMOR_HEADER}\n{encoded}\n"


def parse_seed_bundle(text: str) -> Dict:
    stripped = text.strip()
    if stripped.startswith(ARC_ARMOR_HEADER):
        encoded = "".join(stripped.splitlines()[1:]).strip()
        try:
            decoded = base64.b64decode(encoded, validate=True)
            return json.loads(decoded.decode("utf-8"))
        except Exception as e:
            raise ValueError("Selected encrypted seed file armor is invalid.") from e
    try:
        return json.loads(text)
    except Exception as e:
        raise ValueError("Selected file is not a supported encrypted seed file.") from e


def decrypt(bundle: Dict, password: str) -> str:
    if not isinstance(bundle, dict):
        raise ValueError("Unsupported encrypted seed file format.")
    if bundle.get("magic") == ARC_MAGIC or bundle.get("version") == 2:
        return decrypt_v2(bundle, password)
    return decrypt_v1(bundle, password)


def encrypt_seed_bundle_v1(mnemonic: str, password: str) -> Dict:
    salt = os.urandom(16)
    nonce = os.urandom(16)
    password_bytes = normalize_nfkd(password).encode("utf-8")
    derived = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 250000, dklen=64)
    enc_key, mac_key = derived[:32], derived[32:]
    words = normalize_mnemonic_words(mnemonic)
    payload = {
        "mnemonic": " ".join(words),
        "word_count": len(words),
    }
    plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ciphertext = xor_stream_crypt(plaintext, enc_key, nonce)
    mac = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
    return {
        "format": "yellowsphere-encrypted-seed-v2",
        "kdf": {
            "name": "PBKDF2",
            "hash": "SHA-256",
            "iterations": 250000,
            "salt_b64": base64.b64encode(salt).decode("ascii"),
        },
        "cipher": {
            "name": "XOR-HMAC-SHA256",
            "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        },
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "mac_b64": base64.b64encode(mac).decode("ascii"),
    }


def parse_path(path: str) -> List[int]:
    if not path:
        return []
    elems = path.strip().split("/")
    if elems[0] == "m":
        elems = elems[1:]
    out = []
    for e in elems:
        if e == "":
            continue
        hardened = False
        if e.endswith("'") or e.endswith("h") or e.endswith("H"):
            hardened = True
            e = e[:-1]
        i = int(e)
        if i < 0 or i >= HARDENED:
            raise ValueError(f"invalid path index: {i}")
        if hardened:
            i |= HARDENED
        out.append(i)
    return out


def normalize_path(path: str) -> str:
    ints = parse_path(path)
    if not ints:
        return "m"
    parts = []
    for i in ints:
        parts.append(f"{i - HARDENED}'" if (i & HARDENED) else str(i))
    return "m/" + "/".join(parts)


def purpose_to_script_type(path: str) -> str:
    ints = parse_path(path)
    if not ints:
        return "p2pkh"
    purpose = ints[0] & 0x7FFFFFFF
    if purpose == 44:
        return "p2pkh"
    if purpose == 49:
        return "p2wpkh-p2sh"
    if purpose == 84:
        return "p2wpkh"
    if purpose == 86:
        return "p2tr"
    return "p2pkh"


@dataclass
class ExtPrv:
    k: int
    c: bytes
    depth: int
    parent_fp: bytes
    child_num: int

    def pub(self):
        return point_mul(self.k, G)


def master_from_seed(seed: bytes) -> ExtPrv:
    I = hmac_sha512(b"Bitcoin seed", seed)
    IL, IR = I[:32], I[32:]
    k = int.from_bytes(IL, "big")
    if k == 0 or k >= N:
        raise ValueError("invalid master key")
    return ExtPrv(k=k, c=IR, depth=0, parent_fp=b"\x00\x00\x00\x00", child_num=0)


def ckd_priv(node: ExtPrv, index: int) -> ExtPrv:
    data = (b"\x00" + ser256(node.k) if (index & HARDENED) else ser_pubkey(node.pub())) + ser32(index)
    I = hmac_sha512(node.c, data)
    IL, IR = I[:32], I[32:]
    il_int = int.from_bytes(IL, "big")
    child_k = (il_int + node.k) % N
    if il_int >= N or child_k == 0:
        raise ValueError("invalid child key")
    fp = hash160(ser_pubkey(node.pub()))[:4]
    return ExtPrv(k=child_k, c=IR, depth=node.depth + 1, parent_fp=fp, child_num=index)


def derive(node: ExtPrv, path: str) -> ExtPrv:
    out = node
    for i in parse_path(path):
        out = ckd_priv(out, i)
    return out


def ext_prv_to_base58(node: ExtPrv, version: int) -> str:
    payload = (
        version.to_bytes(4, "big")
        + bytes([node.depth])
        + node.parent_fp
        + ser32(node.child_num)
        + node.c
        + b"\x00"
        + ser256(node.k)
    )
    return b58check(payload)


def ext_pub_to_base58(node: ExtPrv, version: int) -> str:
    payload = (
        version.to_bytes(4, "big")
        + bytes([node.depth])
        + node.parent_fp
        + ser32(node.child_num)
        + node.c
        + ser_pubkey(node.pub())
    )
    return b58check(payload)


def to_wif(privkey: int, netcfg: dict) -> str:
    if netcfg.get("wif") is None:
        raise ValueError("WIF is not defined for this coin/network")
    return b58check(bytes([netcfg["wif"]]) + ser256(privkey) + b"\x01")


def ser_pubkey_uncompressed(p) -> bytes:
    x, y = p
    return x.to_bytes(32, "big") + y.to_bytes(32, "big")


def ethereum_checksum_address(address_bytes: bytes) -> str:
    address_hex = address_bytes.hex()
    hash_hex = keccak256(address_hex.encode("ascii")).hex()
    checked = "".join(c.upper() if int(hash_hex[i], 16) >= 8 else c for i, c in enumerate(address_hex))
    return "0x" + checked


def ethereum_address_from_private_key(privkey: int) -> str:
    pub = point_mul(privkey, G)
    if pub is None:
        raise ValueError("invalid Ethereum public key")
    return ethereum_checksum_address(keccak256(ser_pubkey_uncompressed(pub))[-20:])


def tron_address_from_private_key(privkey: int) -> tuple[str, str]:
    pub = point_mul(privkey, G)
    if pub is None:
        raise ValueError("invalid TRON public key")
    payload = b"\x41" + keccak256(ser_pubkey_uncompressed(pub))[-20:]
    return b58check(payload), payload.hex()


def cosmos_address_from_public_key(pubkey: bytes, hrp: str = "cosmos") -> str:
    return bech32_encode(hrp, convertbits(hash160(pubkey), 8, 5, True))


def xrp_classic_address_from_public_key(pubkey: bytes) -> str:
    return b58check(b"\x00" + hash160(pubkey), XRP_B58_ALPHABET)


def taproot_key_material(privkey: int) -> Dict:
    pub = point_mul(privkey, G)
    if pub is None:
        raise ValueError("invalid Taproot internal key")
    if pub[1] & 1:
        internal_priv = (N - privkey) % N
        internal_pub = negate_point(pub)
    else:
        internal_priv = privkey
        internal_pub = pub
    tweak = int.from_bytes(tagged_hash("TapTweak", xonly_pubkey(internal_pub)), "big")
    if tweak >= N:
        raise ValueError("invalid Taproot tweak")
    output_pub = point_add(internal_pub, point_mul(tweak, G))
    if output_pub is None:
        raise ValueError("invalid Taproot output key")
    output_priv = (internal_priv + tweak) % N
    if output_priv == 0:
        raise ValueError("invalid Taproot private key")
    return {
        "internal_private_key": internal_priv,
        "internal_public_key": xonly_pubkey(internal_pub),
        "tweak": tweak.to_bytes(32, "big"),
        "output_private_key": output_priv,
        "output_public_key": xonly_pubkey(output_pub),
        "output_key_parity": output_pub[1] & 1,
    }


def pubkey_to_address(pubkey: bytes, script_type: str, netcfg: dict) -> str:
    pkh = hash160(pubkey)
    if script_type == "p2pkh":
        if netcfg.get("cashaddr_prefix"):
            return cashaddr_encode(netcfg["cashaddr_prefix"], 0, pkh)
        return b58check(bytes([netcfg["p2pkh_prefix"]]) + pkh)
    if script_type == "p2wpkh":
        return segwit_addr_v0(netcfg["hrp"], pkh)
    if script_type == "p2wpkh-p2sh":
        redeem = b"\x00\x14" + pkh
        return b58check(bytes([netcfg["p2sh_prefix"]]) + hash160(redeem))
    if script_type == "p2tr":
        raise ValueError("taproot addresses require Taproot key material")
    raise ValueError(f"unsupported script type: {script_type}")


def derive_account(mnemonic: str, passphrase: str, derivation: str, script_type: str, count: int, netcfg: dict, start_index: int = 0):
    seed = bip39_to_seed(mnemonic, passphrase)
    root = master_from_seed(seed)
    account = derive(root, derivation)
    address_family = netcfg.get("address_family")
    is_ethereum = address_family == "ethereum"
    is_evm = address_family in ("ethereum", "evm")
    is_tron = address_family == "tron"
    is_cosmos = address_family == "cosmos"
    is_xrp = address_family == "xrp"
    st = address_family if address_family in ("ethereum", "evm", "tron", "cosmos", "xrp") else (purpose_to_script_type(derivation) if script_type == "auto" else script_type)
    root_versions = netcfg["p2pkh"]
    x_versions = netcfg["p2pkh"]
    y_versions = netcfg["p2wpkh-p2sh"]
    z_versions = netcfg["p2wpkh"]
    tr_versions = netcfg["p2tr"]
    if st not in ("ethereum", "evm", "tron", "cosmos", "xrp") and not netcfg.get(st):
        raise ValueError(f"{st} is not supported for this coin/network")
    if st == "p2tr" and not tr_versions:
        raise ValueError("taproot is not supported for this coin/network")

    result = {
        "derivation": derivation,
        "account_script_type_used": st,
        "root_xprv": ext_prv_to_base58(root, root_versions["xprv"]),
        "root_xpub": ext_pub_to_base58(root, root_versions["xpub"]),
    }
    if st == "p2wpkh-p2sh":
        result["root_yprv"] = ext_prv_to_base58(root, y_versions["xprv"])
        result["root_ypub"] = ext_pub_to_base58(root, y_versions["xpub"])
    elif st == "p2wpkh":
        result["root_zprv"] = ext_prv_to_base58(root, z_versions["xprv"])
        result["root_zpub"] = ext_pub_to_base58(root, z_versions["xpub"])
    elif st == "p2tr" and tr_versions:
        result["root_trprv"] = ext_prv_to_base58(root, tr_versions["xprv"])
        result["root_trpub"] = ext_pub_to_base58(root, tr_versions["xpub"])
    result["account_xprv"] = ext_prv_to_base58(account, x_versions["xprv"])
    result["account_xpub"] = ext_pub_to_base58(account, x_versions["xpub"])
    if st == "p2wpkh-p2sh":
        result["account_yprv"] = ext_prv_to_base58(account, y_versions["xprv"])
        result["account_ypub"] = ext_pub_to_base58(account, y_versions["xpub"])
    elif st == "p2wpkh":
        result["account_zprv"] = ext_prv_to_base58(account, z_versions["xprv"])
        result["account_zpub"] = ext_pub_to_base58(account, z_versions["xpub"])
    elif st == "p2tr" and tr_versions:
        result["account_trprv"] = ext_prv_to_base58(account, tr_versions["xprv"])
        result["account_trpub"] = ext_pub_to_base58(account, tr_versions["xpub"])
    result["receiving"] = []
    result["change"] = []

    for branch, key in ((0, "receiving"), (1, "change")):
        branch_node = ckd_priv(account, branch)
        for i in range(start_index, start_index + count):
            child = ckd_priv(branch_node, i)
            pub = ser_pubkey(child.pub())
            item = {
                "path": f"{derivation}/{branch}/{i}",
                "address": None if st in ("p2tr", "ethereum", "evm", "tron", "cosmos", "xrp") else pubkey_to_address(pub, st, netcfg),
                "public_key_hex": pub.hex(),
                "private_key_hex": ser256(child.k).hex(),
            }
            if is_evm:
                item["address"] = ethereum_address_from_private_key(child.k)
                item["evm_public_key_hex"] = ser_pubkey_uncompressed(child.pub()).hex()
                if is_ethereum:
                    item["ethereum_public_key_hex"] = item["evm_public_key_hex"]
                    item["erc20_address"] = item["address"]
                    item["erc20_note"] = "ERC-20 tokens on Ethereum use this same account address."
                else:
                    note_key = netcfg.get("evm_note_key", "evm_note")
                    label = netcfg.get("evm_label", "EVM chain")
                    item[note_key] = f"{label} uses Ethereum-compatible 0x addresses with this same secp256k1 account key."
            elif is_tron:
                item["address"], item["tron_hex_address"] = tron_address_from_private_key(child.k)
                item["trc20_note"] = "TRC-20 tokens on TRON use this same account address."
            elif is_cosmos:
                item["address"] = cosmos_address_from_public_key(pub, netcfg.get("address_hrp", "cosmos"))
                item["cosmos_note"] = "Cosmos Hub account address using secp256k1 and Bech32 HRP cosmos."
            elif is_xrp:
                item["address"] = xrp_classic_address_from_public_key(pub)
                item["xrp_classic_address"] = item["address"]
                item["xrp_note"] = "XRP Ledger classic address. Destination tags, when required by an exchange or custodian, must be supplied separately from the seed."
            else:
                item["private_key_wif"] = to_wif(child.k, netcfg)
            if st == "p2tr":
                taproot = taproot_key_material(child.k)
                item["address"] = segwit_addr_v1(netcfg["hrp"], taproot["output_public_key"])
                item["taproot_internal_public_key_hex"] = taproot["internal_public_key"].hex()
                item["taproot_internal_private_key_hex"] = ser256(taproot["internal_private_key"]).hex()
                item["taproot_internal_private_key_wif"] = to_wif(taproot["internal_private_key"], netcfg)
                item["taproot_tweak_hex"] = taproot["tweak"].hex()
                item["taproot_output_public_key_hex"] = taproot["output_public_key"].hex()
                item["taproot_output_private_key_hex"] = ser256(taproot["output_private_key"]).hex()
                item["taproot_output_private_key_wif"] = to_wif(taproot["output_private_key"], netcfg)
                item["taproot_output_key_parity"] = taproot["output_key_parity"]
            result[key].append(item)
    return result


def _empty_account(derivation: str, script_type: str) -> Dict:
    return {
        "derivation": derivation,
        "account_script_type_used": script_type,
        "receiving": [],
        "change": [],
    }


def derive_solana_output(seed: bytes, derivation: str, count: int, start_index: int, word_count: int, network: str) -> Dict:
    root = master_from_seed_ed25519(seed)
    account = derive_ed25519(root, derivation)
    out_account = _empty_account(derivation, "solana")
    out_account.update(
        {
            "root_private_key_hex": root["k"].hex(),
            "root_chain_code_hex": root["c"].hex(),
            "root_public_key_hex": ed25519_public_key_from_seed(root["k"]).hex(),
            "account_private_key_hex": account["k"].hex(),
            "account_chain_code_hex": account["c"].hex(),
            "account_public_key_hex": ed25519_public_key_from_seed(account["k"]).hex(),
        }
    )
    for i in range(start_index, start_index + count):
        path = solana_path_for_index(derivation, i)
        child = account if i == 0 and normalize_path(path) == normalize_path(derivation) else derive_ed25519(root, path)
        public_key = ed25519_public_key_from_seed(child["k"])
        out_account["receiving"].append(
            {
                "path": path,
                "address": b58encode(public_key),
                "public_key_hex": public_key.hex(),
                "private_key_hex": child["k"].hex(),
            }
        )
    return {"coin": "solana", "network": network, "word_count": word_count, "accounts": [out_account]}


def derive_stellar_output(seed: bytes, derivation: str, count: int, start_index: int, word_count: int, network: str) -> Dict:
    root = master_from_seed_ed25519(seed)
    account = derive_ed25519(root, derivation)
    out_account = _empty_account(derivation, "stellar")
    out_account.update(
        {
            "root_private_key_hex": root["k"].hex(),
            "root_chain_code_hex": root["c"].hex(),
            "root_public_key_hex": ed25519_public_key_from_seed(root["k"]).hex(),
            "account_private_key_hex": account["k"].hex(),
            "account_chain_code_hex": account["c"].hex(),
            "account_public_key_hex": ed25519_public_key_from_seed(account["k"]).hex(),
        }
    )
    for i in range(start_index, start_index + count):
        path = account_path_for_index(derivation, 148, i)
        child = account if i == 0 and normalize_path(path) == normalize_path(derivation) else derive_ed25519(root, path)
        public_key = ed25519_public_key_from_seed(child["k"])
        out_account["receiving"].append(
            {
                "path": path,
                "address": stellar_public_address(public_key),
                "public_key_hex": public_key.hex(),
                "private_key_hex": child["k"].hex(),
                "stellar_secret_seed": stellar_secret_seed(child["k"]),
            }
        )
    return {"coin": "stellar", "network": network, "word_count": word_count, "accounts": [out_account]}


def derive_monero_output(seed: bytes, derivation: str, count: int, start_index: int, word_count: int, network: str) -> Dict:
    root = master_from_seed_ed25519(seed)
    account = derive_ed25519(root, derivation)
    root_spend = reduce_ed25519_scalar(root["k"])
    root_addr = monero_address_from_spend_key(root_spend)
    account_spend = reduce_ed25519_scalar(account["k"])
    account_addr = monero_address_from_spend_key(account_spend)
    out_account = _empty_account(derivation, "monero")
    out_account.update(
        {
            "root_private_key_hex": root["k"].hex(),
            "root_chain_code_hex": root["c"].hex(),
            "root_private_spend_key_hex": root_spend.hex(),
            "root_private_view_key_hex": root_addr["private_view_key"].hex(),
            "root_public_spend_key_hex": root_addr["public_spend_key"].hex(),
            "root_public_view_key_hex": root_addr["public_view_key"].hex(),
            "account_private_key_hex": account["k"].hex(),
            "account_chain_code_hex": account["c"].hex(),
            "account_private_spend_key_hex": account_spend.hex(),
            "account_private_view_key_hex": account_addr["private_view_key"].hex(),
            "account_public_spend_key_hex": account_addr["public_spend_key"].hex(),
            "account_public_view_key_hex": account_addr["public_view_key"].hex(),
        }
    )
    out_account["receiving"].append(
        {
            "path": derivation,
            "address": account_addr["address"],
            "public_spend_key_hex": account_addr["public_spend_key"].hex(),
            "public_view_key_hex": account_addr["public_view_key"].hex(),
            "private_spend_key_hex": account_spend.hex(),
            "private_view_key_hex": account_addr["private_view_key"].hex(),
        }
    )
    return {"coin": "monero", "network": network, "word_count": word_count, "accounts": [out_account]}


def derive_cardano_output(mnemonic: str, passphrase: str, derivation: str, count: int, start_index: int, word_count: int, network: str, netcfg: dict) -> Dict:
    entropy = mnemonic_entropy_bytes(mnemonic)
    root = cardano_icarus_master_from_entropy(entropy, passphrase)
    account = derive_cardano(root, derivation)
    out_account = _empty_account(derivation, "cardano")
    out_account.update(
        {
            "root_private_key_hex": root["k"].hex(),
            "root_chain_code_hex": root["c"].hex(),
            "root_public_key_hex": cardano_public_key_from_private(root["k"]).hex(),
            "account_private_key_hex": account["k"].hex(),
            "account_chain_code_hex": account["c"].hex(),
            "account_public_key_hex": cardano_public_key_from_private(account["k"]).hex(),
        }
    )
    for i in range(start_index, start_index + count):
        paths = cardano_paths_for_index(derivation, i)
        payment = account if i == 0 and normalize_path(paths["payment_path"]) == normalize_path(derivation) else derive_cardano(root, paths["payment_path"])
        staking = derive_cardano(root, paths["staking_path"])
        payment_pub = cardano_public_key_from_private(payment["k"])
        staking_pub = cardano_public_key_from_private(staking["k"])
        out_account["receiving"].append(
            {
                "path": paths["payment_path"],
                "staking_path": paths["staking_path"],
                "address": cardano_shelley_base_address(
                    payment_pub,
                    staking_pub,
                    netcfg.get("network_id", 1),
                    netcfg.get("address_hrp", "addr"),
                ),
                "public_key_hex": payment_pub.hex(),
                "stake_public_key_hex": staking_pub.hex(),
                "private_key_hex": payment["k"].hex(),
                "stake_private_key_hex": staking["k"].hex(),
            }
        )
    return {"coin": "cardano", "network": network, "word_count": word_count, "accounts": [out_account]}


def run_derivation(
    mnemonic: str,
    passphrase: str,
    derivation: str,
    all_common: bool,
    script_type: str,
    count: int,
    coin: str,
    testnet: bool,
    start_index: int = 0,
) -> Dict:
    words_ok, checksum_ok, msg = bip39_validate(mnemonic)
    if not words_ok:
        raise ValueError(msg)
    if not checksum_ok:
        raise ValueError(msg)
    if count < 1:
        raise ValueError("--count must be >= 1")

    coin_key = coin.strip().lower()
    if coin_key not in COINS:
        raise ValueError(f"unsupported coin: {coin}")
    coin_cfg = COINS[coin_key]
    if testnet:
        if coin_cfg["testnet"] is None:
            raise ValueError(f"testnet is not configured for {coin_key}")
        netcfg = coin_cfg["testnet"]
    else:
        netcfg = coin_cfg["mainnet"]

    coin_type = coin_cfg["coin_type"]
    base_derivation = (derivation or "").strip()
    if not base_derivation and testnet and coin_key in ("bitcoin", "bitcoincash", "litecoin", "dogecoin"):
        default_script = script_type if script_type != "auto" else ("p2wpkh" if coin_key in ("bitcoin", "litecoin") else "p2pkh")
        base_derivation = TESTNET_UTXO_DERIVATION[default_script]
    if not base_derivation:
        base_derivation = DEFAULT_ACCOUNT_DERIVATION[coin_key]
    base_derivation = normalize_path(base_derivation)
    network_name = "testnet" if testnet else "mainnet"
    word_count = len(normalize_mnemonic_words(mnemonic))
    address_family = netcfg.get("address_family")
    if address_family == "solana":
        return derive_solana_output(bip39_to_seed(mnemonic, passphrase), base_derivation, count, start_index, word_count, network_name)
    if address_family == "stellar":
        return derive_stellar_output(bip39_to_seed(mnemonic, passphrase), base_derivation, count, start_index, word_count, network_name)
    if address_family == "cardano":
        return derive_cardano_output(mnemonic, passphrase, base_derivation, count, start_index, word_count, network_name, netcfg)

    if all_common and address_family in ("ethereum", "evm", "tron", "cosmos", "xrp"):
        derivations = [f"m/44'/{coin_type}'/0'"]
    elif all_common and coin_key == "bitcoincash":
        derivations = [f"m/44'/{coin_type}'/0'"]
    else:
        derivations = (
            [f"m/44'/{coin_type}'/0'", f"m/49'/{coin_type}'/0'", f"m/84'/{coin_type}'/0'", f"m/86'/{coin_type}'/0'"] if all_common else [base_derivation]
        )
    derivations = [normalize_path(d) for d in derivations]

    out = {
        "coin": coin_key,
        "network": network_name,
        "word_count": word_count,
        "accounts": [],
    }
    for d in derivations:
        out["accounts"].append(derive_account(mnemonic, passphrase, d, script_type, count, netcfg, start_index))
    return out


def flatten_derived_rows(data: Dict) -> List[Dict]:
    rows = []
    for account in data.get("accounts", []):
        account_fields = {k: v for k, v in account.items() if k not in ("receiving", "change")}
        for branch in ("receiving", "change"):
            for item in account.get(branch, []):
                rows.append(
                    {
                        "coin": data.get("coin"),
                        "network": data.get("network"),
                        "word_count": data.get("word_count"),
                        "branch": branch,
                        **account_fields,
                        **item,
                    }
                )
    return rows


def derived_to_csv(data: Dict) -> str:
    rows = flatten_derived_rows(data)
    if not rows:
        return ""
    headers = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def text_label(key: str) -> str:
    return key.replace("_", " ")


def append_text_fields(lines: List[str], obj: Dict, exclude: Tuple[str, ...] = ()) -> None:
    excluded = set(exclude)
    for key, value in (obj or {}).items():
        if key in excluded or value is None:
            continue
        lines.append(f"{text_label(key)}: {value}")


def derived_to_text(data: Dict) -> str:
    lines = [
        "YellowSphere Derived Keys and Addresses",
        "",
        f"coin: {data.get('coin', '')}",
        f"network: {data.get('network', '')}",
        f"word count: {data.get('word_count', '')}",
    ]
    for account_index, account in enumerate(data.get("accounts", []), start=1):
        lines.extend(["", f"Account {account_index}"])
        append_text_fields(lines, account, ("receiving", "change"))
        for branch in ("receiving", "change"):
            lines.extend(["", f"{branch.capitalize()} Addresses"])
            items = account.get(branch, [])
            if not items:
                lines.append("No addresses derived.")
                continue
            for item_index, item in enumerate(items):
                lines.extend(["", f"{branch} #{item_index}"])
                append_text_fields(lines, item)
    return "\n".join(lines) + "\n"


def format_derived_output(data: Dict, output_format: str) -> str:
    fmt = output_format.lower()
    if fmt == "csv":
        return derived_to_csv(data)
    if fmt == "txt":
        return derived_to_text(data)
    return json.dumps(data, indent=2) + "\n"


def _pdf_escape(text: object) -> str:
    value = "" if text is None else str(text)
    value = value.encode("latin-1", "replace").decode("latin-1")
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _pdf_clip(text: object, max_chars: int) -> str:
    value = "" if text is None else str(text)
    if len(value) <= max_chars:
        return value
    return value[: max(1, max_chars - 3)] + "..."


def _coin_display_name(coin: str) -> str:
    return {
        "bitcoin": "Bitcoin",
        "bitcoincash": "Bitcoin Cash",
        "litecoin": "Litecoin",
        "dogecoin": "Dogecoin",
        "ethereum": "Ethereum",
        "bnbchain": "BNB Chain",
        "avalanche": "Avalanche C-Chain",
        "polygon": "Polygon",
        "tron": "Tron",
        "cosmos": "Cosmos / ATOM",
        "solana": "Solana",
        "stellar": "Stellar",
        "cardano": "Cardano",
        "xrp": "XRP",
    }.get(coin, coin or "export")


def _pdf_text(commands: List[str], x: float, y: float, text: object, size: float = 8, bold: bool = False) -> None:
    font = "F2" if bold else "F1"
    commands.append(f"BT /{font} {size:g} Tf {x:.2f} {y:.2f} Td ({_pdf_escape(text)}) Tj ET")


def _write_simple_pdf(path: str, page_streams: List[str], width: float = 841.89, height: float = 595.28) -> None:
    objects: List[bytes] = []

    def add(obj: str | bytes) -> int:
        objects.append(obj.encode("latin-1") if isinstance(obj, str) else obj)
        return len(objects)

    catalog_id = add("PLACEHOLDER")
    pages_id = add("PLACEHOLDER")
    font_regular_id = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    font_bold_id = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    page_ids: List[int] = []

    for stream in page_streams:
        data = stream.encode("latin-1", "replace")
        content_id = add(b"<< /Length " + str(len(data)).encode("ascii") + b" >>\nstream\n" + data + b"\nendstream")
        page_id = add(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {width:.2f} {height:.2f}] "
            f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        )
        page_ids.append(page_id)

    objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("latin-1")
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1")

    with open(path, "wb") as f:
        f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for obj_id, obj in enumerate(objects, start=1):
            offsets.append(f.tell())
            f.write(f"{obj_id} 0 obj\n".encode("ascii"))
            f.write(obj)
            f.write(b"\nendobj\n")
        xref_at = f.tell()
        f.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        f.write(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            f.write(f"{off:010d} 00000 n \n".encode("ascii"))
        f.write(
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_at}\n%%EOF\n".encode("ascii")
        )


def save_derived_pdf(data: Dict, path: str, root_fingerprint: str = "") -> None:
    rows = flatten_derived_rows(data)
    if not rows:
        raise ValueError("No rows to export.")

    page_w, page_h = 841.89, 595.28
    margin = 36
    row_h = 14
    table_top_gap = 18
    bottom = margin
    usable_w = page_w - (margin * 2)
    coin = _coin_display_name(str(data.get("coin", "")))
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    root_fp = (root_fingerprint or "").strip()
    if root_fp.lower().startswith("root fingerprint:"):
        root_fp = root_fp.split(":", 1)[1].strip()

    coin_id = data.get("coin")
    is_hex_key_coin = coin_id in ("ethereum", "bnbchain", "avalanche", "polygon", "tron", "cosmos", "solana", "stellar", "cardano", "xrp")
    private_col = "private_key_hex" if is_hex_key_coin else "private_key_wif"
    private_header = "PRIVATE KEY HEX" if is_hex_key_coin else "PRIVATE KEY WIF"
    cols = [
        ("branch", "BRANCH", 52, 9),
        ("path", "PATH", 110, 22),
        ("address", "ADDRESS", 270, 46),
        (private_col, private_header, usable_w - 52 - 110 - 270 - 18, 52),
    ]

    account = (data.get("accounts") or [{}])[0] or {}
    key_labels = {
        "root_xprv": "root xprv", "root_xpub": "root xpub",
        "root_yprv": "root yprv", "root_ypub": "root ypub",
        "root_zprv": "root zprv", "root_zpub": "root zpub",
        "root_trprv": "root trprv", "root_trpub": "root trpub",
        "account_xprv": "account xprv", "account_xpub": "account xpub",
        "account_yprv": "account yprv", "account_ypub": "account ypub",
        "account_zprv": "account zprv", "account_zpub": "account zpub",
        "account_trprv": "account trprv", "account_trpub": "account trpub",
    }
    key_pairs = [(label, account[key]) for key, label in key_labels.items() if account.get(key)]

    streams: List[str] = []
    commands: List[str] = []
    y = page_h - margin
    page_num = 1

    def new_page() -> None:
        nonlocal commands, y, page_num
        if commands:
            streams.append("\n".join(commands))
        commands = []
        y = page_h - margin
        page_num += 1
        draw_title()
        draw_table_header()

    def draw_title() -> None:
        nonlocal y
        _pdf_text(commands, margin, y, "YellowSphere Key Export", 13, True)
        meta = [coin, f"YellowSphere v{APP_VERSION}", timestamp]
        if root_fp:
            meta.append(f"Fingerprint: {root_fp}")
        _pdf_text(commands, margin, y - 14, "  |  ".join(meta), 8)
        _pdf_text(commands, page_w - margin - 42, y - 14, f"Page {page_num}", 8)
        y -= 34

    def draw_extended_keys() -> None:
        nonlocal y
        if not key_pairs:
            return
        _pdf_text(commands, margin, y, "EXTENDED KEYS", 8, True)
        y -= 12
        for label, value in key_pairs:
            if y < bottom + row_h + table_top_gap:
                new_page()
            _pdf_text(commands, margin, y, label.upper(), 7, True)
            _pdf_text(commands, margin + 90, y, _pdf_clip(value, 118), 7.5)
            y -= 13
        y -= 8

    def draw_table_header() -> None:
        nonlocal y
        x = margin
        for _key, label, width, _chars in cols:
            _pdf_text(commands, x, y, label, 7, True)
            x += width + 6
        y -= 13

    draw_title()
    draw_extended_keys()
    y -= table_top_gap
    draw_table_header()

    for row in rows:
        if y < bottom + row_h:
            new_page()
        x = margin
        for key, _label, width, chars in cols:
            value = _pdf_clip(row.get(key, ""), chars)
            _pdf_text(commands, x, y, value, 7.5, bold=(key == "branch"))
            x += width + 6
        y -= row_h

    streams.append("\n".join(commands))
    _write_simple_pdf(path, streams, page_w, page_h)


                                                                             
                                                                      
                                                                             
import re as _re
import zlib as _zlib
import struct as _struct

_QR_EXP = [0] * 512
_QR_LOG = [0] * 256

def _build_gf():
    x = 1
    for i in range(255):
        _QR_EXP[i] = x; _QR_LOG[x] = i
        x = x << 1
        if x > 255: x ^= 0x11d
    for i in range(255, 512): _QR_EXP[i] = _QR_EXP[i - 255]

_build_gf()

def _gf_mul(a, b): return _QR_EXP[_QR_LOG[a] + _QR_LOG[b]] if a and b else 0

def _gf_poly(ec):
    p = [1]
    for i in range(ec):
        q = [1, _QR_EXP[i]]
        r = [0] * (len(p) + 1)
        for a in range(len(p)):
            for b in range(len(q)):
                r[a + b] ^= _gf_mul(p[a], q[b])
        p = r
    return p

def _rs_encode(data, ec):
    gen = _gf_poly(ec)
    out = list(data) + [0] * ec
    for i in range(len(data)):
        c = out[i]
        if c:
            for j in range(len(gen)):
                out[i + j] ^= _gf_mul(gen[j], c)
    return out[len(data):]

_QR_CAP = [
    None,
    [{"db":16,"ec":10,"b":1},{"db":13,"ec":13,"b":1}],
    [{"db":28,"ec":16,"b":1},{"db":22,"ec":22,"b":1}],
    [{"db":44,"ec":26,"b":2},{"db":32,"ec":18,"b":2}],
    [{"db":64,"ec":18,"b":2},{"db":48,"ec":26,"b":2}],
    [{"db":86,"ec":24,"b":2},{"db":64,"ec":18,"b":4}],
    [{"db":108,"ec":16,"b":4},{"db":84,"ec":24,"b":4}],
    [{"db":124,"ec":18,"b":4},{"db":93,"ec":18,"b":6}],
    [{"db":154,"ec":22,"b":4},{"db":122,"ec":22,"b":6}],
    [{"db":182,"ec":22,"b":5},{"db":154,"ec":20,"b":7}],
    [{"db":216,"ec":26,"b":5},{"db":180,"ec":24,"b":8}],
]

_FMT_M = [0b101010000010010,0b101000100100101,0b101111001111100,0b101101101001011,
           0b100010111111001,0b100000011001110,0b100111110010111,0b100101010100000]
_FMT_Q = [0b011010101011111,0b011000001101000,0b011111100110001,0b011101000000110,
           0b010010010110100,0b010000110000011,0b010111011011010,0b010101111101101]

_QR_ALIGN = [None,[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50]]

def _qr_make_matrix(ver):
    size = ver * 4 + 17
    m = [[0]*size for _ in range(size)]
    def rect(r,c,h,w,v):
        for dr in range(h):
            for dc in range(w):
                m[r+dr][c+dc] = v
    def finder(r,c):
        rect(r,c,7,7,1); rect(r+1,c+1,5,5,0); rect(r+2,c+2,3,3,1)
    finder(0,0); finder(0,size-7); finder(size-7,0)
                
    for i in range(8):
        for pos in [(7,i),(i,7),(7,size-8+i),(size-8+i,7),(7,i),(size-8+i,size-8)]:
            if 0<=pos[0]<size and 0<=pos[1]<size: m[pos[0]][pos[1]]=0
        m[7][i]=0; m[i][7]=0
        m[7][size-8+i]=0; m[size-8+i][7]=0
        m[size-8][i]=0; m[i][size-8]=0
        m[7][size-1-i]=0 if i<8 else m[7][size-1-i]
            
    for i in range(8,size-8):
        m[6][i] = 1 if i%2==0 else 0
        m[i][6] = 1 if i%2==0 else 0
               
    aligns = _QR_ALIGN[ver]
    for ar in aligns:
        for ac in aligns:
            if m[ar][ac] == 0 or (ar==6 and ac==6):
                pass
            else:
                rect(ar-2,ac-2,5,5,1); rect(ar-1,ac-1,3,3,0); m[ar][ac]=1
                 
    m[size-8][8] = 1
                                                                            
    fmt_positions = (
        [(8,i) for i in range(9) if i!=6] + [(7,8),(5,8),(4,8),(3,8),(2,8),(1,8),(0,8)] +
        [(i,size-1-j) for j,i in enumerate(range(8))] + [(size-7+j,8) for j in range(7)]
    )
    for (r,c) in fmt_positions:
        if 0<=r<size and 0<=c<size: m[r][c]=0
                                     
    for r in range(size):
        for c in range(size):
            if m[r][c] == 0:
                m[r][c] = False
    return m

def _qr_place_data(m, data):
    size = len(m)
    col = size-1; row = size-1; going_up = True; bit_idx = 0
    while col >= 0:
        if col == 6: col -= 1
        cols = [col, col-1]
        while 0 <= row < size:
            for c in cols:
                if isinstance(m[row][c], bool):
                    if bit_idx < len(data):
                        byte_i = bit_idx // 8
                        bit_i = 7 - (bit_idx % 8)
                        m[row][c] = bool((data[byte_i] >> bit_i) & 1)
                    else:
                        m[row][c] = False
                    bit_idx += 1
            row += -1 if going_up else 1
        going_up = not going_up
        row = 0 if going_up else size-1
        col -= 2

def _mask_fn(mask):
    fns = [
        lambda r,c: (r+c)%2==0,
        lambda r,c: r%2==0,
        lambda r,c: c%3==0,
        lambda r,c: (r+c)%3==0,
        lambda r,c: (r//2+c//3)%2==0,
        lambda r,c: (r*c)%2+(r*c)%3==0,
        lambda r,c: ((r*c)%2+(r*c)%3)%2==0,
        lambda r,c: ((r+c)%2+(r*c)%3)%2==0,
    ]
    return fns[mask]

def _qr_apply_mask(m, mask):
    size = len(m)
    out = [row[:] for row in m]
    fn = _mask_fn(mask)
    for r in range(size):
        for c in range(size):
            if isinstance(out[r][c], bool):
                out[r][c] = out[r][c] != fn(r,c)
    return out

def _qr_write_format(m, ec_level, mask):
    size = len(m)
    fmt = _FMT_M[mask] if ec_level == 'M' else _FMT_Q[mask]
    bits = [(fmt >> (14-i)) & 1 for i in range(15)]
    positions_a = [(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,7),(8,8),(7,8),(5,8),(4,8),(3,8),(2,8),(1,8),(0,8)]
    positions_b = [(size-1,8),(size-2,8),(size-3,8),(size-4,8),(size-5,8),(size-6,8),(size-7,8),(8,size-8),(8,size-7),(8,size-6),(8,size-5),(8,size-4),(8,size-3),(8,size-2),(8,size-1)]
    for i,(r,c) in enumerate(positions_a):
        m[r][c] = bits[i]
    for i,(r,c) in enumerate(positions_b):
        m[r][c] = bits[i]

def _qr_penalty(m):
    size = len(m)
    score = 0
    def v(r,c): return 1 if bool(m[r][c]) else 0
                        
    for r in range(size):
        run=1
        for c in range(1,size):
            if v(r,c)==v(r,c-1): run+=1
            else:
                if run>=5: score+=run-2
                run=1
        if run>=5: score+=run-2
    for c in range(size):
        run=1
        for r in range(1,size):
            if v(r,c)==v(r-1,c): run+=1
            else:
                if run>=5: score+=run-2
                run=1
        if run>=5: score+=run-2
                        
    for r in range(size-1):
        for c in range(size-1):
            a=v(r,c); b=v(r,c+1); d=v(r+1,c); e=v(r+1,c+1)
            if a==b==d==e: score+=3
                      
    pat1=[1,0,1,1,1,0,1,0,0,0,0]; pat2=[0,0,0,0,1,0,1,1,1,0,1]
    for r in range(size):
        for c in range(size-10):
            row=[v(r,c+k) for k in range(11)]
            if row==pat1 or row==pat2: score+=40
    for c in range(size):
        for r in range(size-10):
            col=[v(r+k,c) for k in range(11)]
            if col==pat1 or col==pat2: score+=40
                             
    total=size*size; dark=sum(v(r,c) for r in range(size) for c in range(size))
    pct=100*dark//total; score+=10*min(abs(pct-50)//5, abs((pct+1)-50)//5)
    return score

def _qr_build_codewords(bits, total_data, ec_per_block, num_blocks):
                                
    while len(bits) < total_data*8:
        bits += [1,1,1,0,1,1,0,0] if (len(bits)//8)%2==0 else [0,0,0,1,0,0,0,1]
        if len(bits) >= total_data*8: break
    data_bytes = [int(''.join(map(str,bits[i*8:(i+1)*8])),2) for i in range(total_data)]
                       
    block_sizes = [total_data//num_blocks + (1 if i < total_data%num_blocks else 0) for i in range(num_blocks)]
    blocks=[]; ec_blocks=[]
    idx=0
    for bs in block_sizes:
        blk=data_bytes[idx:idx+bs]; blocks.append(blk); ec_blocks.append(_rs_encode(blk,ec_per_block)); idx+=bs
                
    result=[]
    max_len=max(len(b) for b in blocks)
    for i in range(max_len):
        for b in blocks:
            if i<len(b): result.append(b[i])
    for i in range(ec_per_block):
        for eb in ec_blocks: result.append(eb[i])
    return result

def qr_generate(text: str) -> list:
    data = text.encode('iso-8859-1') if all(ord(c)<256 for c in text) else text.encode('utf-8')
    mode = 0b0100             
    for ver in range(1,11):
        for ecc_idx, ec_level in enumerate(['M','Q']):
            cap = _QR_CAP[ver][ecc_idx]
            if cap['db'] >= len(data)+3:
                break
        else: continue
        break
    else:
        ver=10; ecc_idx=0; ec_level='M'; cap=_QR_CAP[10][0]
    n=len(data); bits=[0]*4; bits[0]=(mode>>3)&1; bits[1]=(mode>>2)&1; bits[2]=(mode>>1)&1; bits[3]=mode&1
                  
    for i in range(7,-1,-1): bits.append((n>>i)&1)
    for byte in data:
        for i in range(7,-1,-1): bits.append((byte>>i)&1)
    bits+=[0,0,0,0]
    codewords=_qr_build_codewords(bits,cap['db'],cap['ec'],cap['b'])
    m=_qr_make_matrix(ver)
    _qr_place_data(m,codewords)
    best=None; best_score=None
    for mask in range(8):
        candidate=_qr_apply_mask(m,mask)
        _qr_write_format(candidate,ec_level,mask)
        s=_qr_penalty(candidate)
        if best_score is None or s<best_score: best_score=s; best=candidate; best_mask=mask
    _qr_write_format(best,ec_level,best_mask)
    return best

def qr_render_canvas(matrix, canvas, module_px=3, quiet=4):
    size = len(matrix)
    total = size + quiet * 2
    dim = total * module_px
    canvas.config(width=dim, height=dim)
    canvas.delete("all")
    canvas.create_rectangle(0, 0, dim, dim, fill="#ffffff", outline="")
    for r in range(size):
        for c in range(size):
            if matrix[r][c]:
                x0 = (c + quiet) * module_px
                y0 = (r + quiet) * module_px
                canvas.create_rectangle(x0, y0, x0+module_px, y0+module_px, fill="#000000", outline="")

def qr_save_png(matrix, path: str, module_px: int = 3, quiet: int = 4):
    size = len(matrix)
    total = size + quiet * 2
    dim = total * module_px
    rows = []
    for ry in range(dim):
        row = bytearray()
        my = ry // module_px - quiet
        for rx in range(dim):
            mx = rx // module_px - quiet
            dark = (0 <= my < size and 0 <= mx < size and matrix[my][mx])
            row += b'\x00\x00\x00' if dark else b'\xff\xff\xff'
        rows.append(b'\x00' + bytes(row))
    compressed = _zlib.compress(b''.join(rows), 9)
    def chunk(name, data):
        c = name + data
        return _struct.pack('>I', len(data)) + c + _struct.pack('>I', _zlib.crc32(c) & 0xffffffff)
    ihdr = _struct.pack('>IIBBBBB', dim, dim, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)

def is_xrp_address(a: str) -> bool:
    return bool(_re.match(r'^r[1-9A-HJ-NP-Za-km-z]{24,}', a.strip()))

def to_bip21_uri(address: str, memo: str = '', coin_context: str = '') -> str:
    a = address.strip()
    m = (memo or '').strip()
    coin = (coin_context or '').strip().lower()
    if _re.match(r'^[a-zA-Z]+:', a): return a
    if coin == 'solana': return 'solana:' + a
    if coin == 'stellar': return 'web+stellar:pay?destination=' + quote(a, safe='')
    if coin == 'cardano': return a
    if coin == 'tron': return 'tron:' + a
    if coin == 'bnbchain': return 'bnb:' + a
    if coin == 'avalanche': return 'avalanche:' + a
    if coin == 'polygon': return 'polygon:' + a
    if coin == 'cosmos': return 'cosmos:' + a
    if coin == 'bitcoincash': return 'bitcoincash:' + a
    if _re.match(r'^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,}', a): return 'bitcoin:' + a
    if _re.match(r'^[qp][023456789acdefghjklmnpqrstuvwxyz]{41,}', a): return 'bitcoincash:' + a
    if _re.match(r'^(ltc1|[LM])[a-zA-HJ-NP-Z0-9]{25,}', a): return 'litecoin:' + a
    if _re.match(r'^[DA9][a-zA-HJ-NP-Z0-9]{25,}', a): return 'dogecoin:' + a
    if _re.match(r'^0x[0-9a-fA-F]{40}$', a): return 'ethereum:' + a
    if is_xrp_address(a): return a + '?dt=' + (quote(m, safe='') if m else '00000')
    return a
