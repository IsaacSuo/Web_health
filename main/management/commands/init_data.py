from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time
from django.contrib.auth.models import User
from main.models import TimeSlot, AcupointMassage


class Command(BaseCommand):
    help = '初始化十二时辰数据、穴位数据和管理员用户'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')
        
        # 初始化管理员用户
        self.init_admin_user()
        
        # 初始化十二时辰数据
        self.init_time_slots()
        
        # 初始化穴位数据
        self.init_acupoints()
        
        self.stdout.write(self.style.SUCCESS('数据初始化完成！'))

    def init_admin_user(self):
        """初始化管理员用户"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('超级用户已创建: admin/admin123'))
        else:
            self.stdout.write('超级用户已存在: admin/admin123')

    def init_time_slots(self):
        """初始化十二时辰数据"""
        time_slots_data = [
            {
                'name': 'zi',
                'chinese_name': '子时',
                'meridian': '足少阳胆经',
                'organ': '胆',
                'start_time': time(23, 0),
                'end_time': time(1, 0),
                'description': '血气流注于胆，称足少阳胆经。此时天地磁场强，胆经引导阳气下降，是身体休养修复开端，子时前入睡胆能完成代谢。"胆汁清，脑清晰"，子时前入睡者晨醒后头脑清、气色好无黑眼圈。反之，常此时不睡则气色差、眼眶黑，胆汁排泄代谢不良易生结晶结石，熬夜还会致胆火上逆，引发失眠头痛、情绪问题等症状，宜多休养。',
                'health_tips': '不要熬夜，子时睡觉很重要。《黄帝内经》认为子时阴气重，之后阴衰阳长，应深度睡眠。',
                'case_suggestions': '经常挠头可刺激胆经活络，助决断。年轻人两耳上部白发，多因胆经气血不足，子时熬夜未休息是重要原因。胆经功能不足会使人胆小多疑、做事没主张。建议子时梳理胆经，用经络梳顺着头部胆经梳理，长期坚持可缓解焦虑，利于睡眠身心健康。',
                'food_recommendations': '番茄凉性甘酸味，生津止渴，适用于夏天汗多或饮水少致的津液不足、口干口渴、尿少等情况。生西红柿（去皮）30-50g切片或打烂，加冰糖内服。还可消食除积，用于暴饮暴食、宿食停积不化致的腹胀、嗳气、食欲减退甚至厌食口干等症状。'
            },
            {
                'name': 'chou',
                'chinese_name': '丑时',
                'meridian': '足厥阴肝经',
                'organ': '肝',
                'start_time': time(1, 0),
                'end_time': time(3, 0),
                'description': '血气流注于肝，称足厥阴肝经。肝有藏血功能，人体血液需要经过肝脏解毒。丑时入眠，肝血推陈出新，将含毒老旧血液淘汰，产生新鲜血液，百脉得以修复，人体得以正常运转。',
                'health_tips': '保持熟睡状态，让肝脏充分解毒和造血。避免在此时熬夜，以免影响肝脏功能。',
                'case_suggestions': '肝火旺的人容易在丑时醒来，表现为烦躁、易怒。建议平时多按压太冲穴，饮食清淡，控制情绪。肝血不足者容易失眠多梦，可适当补充维生素B族。',
                'food_recommendations': '适合食用养肝食物，如枸杞、红枣、桑葚等。避免辛辣刺激食物，减轻肝脏负担。'
            },
            {
                'name': 'yin',
                'chinese_name': '寅时',
                'meridian': '手太阴肺经',
                'organ': '肺',
                'start_time': time(3, 0),
                'end_time': time(5, 0),
                'description': '血气流注于肺，称手太阴肺经。寅时是肺经当令时间，此时肺朝百脉，将肝贮藏的新鲜血液运输全身，送给各脏腑，满足机体的需求。',
                'health_tips': '保持深度睡眠，让肺充分工作。室内保持空气流通，有助于肺的宣泄功能。有肺病者往往在此时咳嗽加剧。',
                'case_suggestions': '肺功能不佳者容易在寅时醒来咳嗽。建议睡前做深呼吸练习，室内放置加湿器。平时多食用白色食物润肺，如梨、百合、银耳等。',
                'food_recommendations': '润肺食物：梨、百合、银耳、莲子、杏仁等。避免寒凉食物，以免伤及肺气。'
            },
            {
                'name': 'mao',
                'chinese_name': '卯时',
                'meridian': '手阳明大肠经',
                'organ': '大肠',
                'start_time': time(5, 0),
                'end_time': time(7, 0),
                'description': '血气流注于大肠，称手阳明大肠经。卯时大肠经旺，有利于排泄，此时起床后应及时排便，清除体内垃圾毒素。',
                'health_tips': '晨起喝温水，按摩腹部，养成定时排便的习惯。适量运动促进肠道蠕动。',
                'case_suggestions': '便秘者应在此时重点调理，可按摩天枢穴、大肠俞等穴位。建议晨起后先喝一杯温开水，然后进行腹部按摩。',
                'food_recommendations': '富含纤维的食物：燕麦、苹果、蔬菜等。适量饮水，促进肠道蠕动。'
            },
            {
                'name': 'chen',
                'chinese_name': '辰时',
                'meridian': '足阳明胃经',
                'organ': '胃',
                'start_time': time(7, 0),
                'end_time': time(9, 0),
                'description': '血气流注于胃，称足阳明胃经。辰时胃经最旺，消化能力最强，是营养能够最好地被消化和吸收的时间。',
                'health_tips': '吃好早餐，为一天提供充足能量。早餐宜营养丰富，易消化。避免生冷食物。',
                'case_suggestions': '胃病患者应特别重视辰时的调养，按时吃早餐，可按摩足三里穴健胃。胃火重者容易口臭，宜清淡饮食。',
                'food_recommendations': '温热易消化的食物：粥、面条、鸡蛋、牛奶等。避免辛辣刺激和生冷食物。'
            },
            {
                'name': 'si',
                'chinese_name': '巳时',
                'meridian': '足太阴脾经',
                'organ': '脾',
                'start_time': time(9, 0),
                'end_time': time(11, 0),
                'description': '血气流注于脾，称足太阴脾经。脾是消化、吸收、排泄的总调度，又是人体血液的统领。脾气不足，易患血液病。',
                'health_tips': '多喝水，避免食用刺激食物。适量运动，但不宜过于剧烈。注意情绪调节，脾主思。',
                'case_suggestions': '脾虚者容易出现消化不良、乏力等症状。建议适当运动，按摩脾俞穴、太白穴。思虑过度伤脾，要注意放松心情。',
                'food_recommendations': '健脾食物：山药、莲子、薏米、红枣、蜂蜜等。避免生冷油腻食物。'
            },
            {
                'name': 'wu',
                'chinese_name': '午时',
                'meridian': '手少阴心经',
                'organ': '心',
                'start_time': time(11, 0),
                'end_time': time(13, 0),
                'description': '血气流注于心，称手少阴心经。心主血脉，主神明。午时心经旺盛，是养心的最佳时机。',
                'health_tips': '适度午睡，但不宜超过30分钟。保持心情愉悦，避免激动。适量补充水分。',
                'case_suggestions': '心脏病患者应注意午时的调养，可按摩内关穴、神门穴。失眠者午睡时间不宜过长，以免影响夜间睡眠。',
                'food_recommendations': '养心食物：红豆、莲子心、百合、桂圆等。避免大量饮酒和浓茶。'
            },
            {
                'name': 'wei',
                'chinese_name': '未时',
                'meridian': '手太阳小肠经',
                'organ': '小肠',
                'start_time': time(13, 0),
                'end_time': time(15, 0),
                'description': '血气流注于小肠，称手太阳小肠经。小肠分清浊，把水液归于膀胱，糟粕送入大肠，精华上输于脾。',
                'health_tips': '吃好午餐，保证营养充足。餐后适当休息，不宜立即剧烈运动。多饮温水。',
                'case_suggestions': '小肠功能不佳者容易出现腹痛、消化不良。建议按摩小肠俞穴，饭后散步促进消化。',
                'food_recommendations': '易消化的食物：瘦肉、鱼类、蔬菜等。避免过于油腻的食物。'
            },
            {
                'name': 'shen',
                'chinese_name': '申时',
                'meridian': '足太阳膀胱经',
                'organ': '膀胱',
                'start_time': time(15, 0),
                'end_time': time(17, 0),
                'description': '血气流注于膀胱，称足太阳膀胱经。膀胱经从头走足，贯穿人体，是最大的排毒通道。',
                'health_tips': '多喝水，促进新陈代谢。适量运动，促进血液循环。注意保暖，避免受寒。',
                'case_suggestions': '膀胱经不通者容易头痛、颈椎病。建议做伸展运动，按摩委中穴。多晒太阳，补充阳气。',
                'food_recommendations': '利水食物：冬瓜、薏米、玉米须茶等。保持充足的水分摄入。'
            },
            {
                'name': 'you',
                'chinese_name': '酉时',
                'meridian': '足少阴肾经',
                'organ': '肾',
                'start_time': time(17, 0),
                'end_time': time(19, 0),
                'description': '血气流注于肾，称足少阴肾经。肾藏精，为先天之本。酉时肾经旺，有利于贮藏一日的脏腑之精华。',
                'health_tips': '减少外出活动，开始为休息做准备。避免过度劳累，保护肾精。可做一些轻柔的运动。',
                'case_suggestions': '肾虚者在此时容易感到疲劳。建议按摩涌泉穴、太溪穴。避免房事过度，节制欲望。',
                'food_recommendations': '补肾食物：黑豆、黑芝麻、核桃、枸杞等。避免寒凉食物。'
            },
            {
                'name': 'xu',
                'chinese_name': '戌时',
                'meridian': '手厥阴心包经',
                'organ': '心包',
                'start_time': time(19, 0),
                'end_time': time(21, 0),
                'description': '血气流注于心包，称手厥阴心包经。心包是心的保护膜，戌时心包经旺，清除心脏周围毒素，保护心脏。',
                'health_tips': '保持心情舒畅，准备进入休息状态。可进行轻松的娱乐活动，避免过度兴奋。',
                'case_suggestions': '心包经不通者容易胸闷、心悸。建议按摩内关穴、膻中穴。避免在此时进行激烈运动。',
                'food_recommendations': '清淡易消化的晚餐，不宜过饱。可饮用安神茶，如菊花茶、薄荷茶等。'
            },
            {
                'name': 'hai',
                'chinese_name': '亥时',
                'meridian': '手少阳三焦经',
                'organ': '三焦',
                'start_time': time(21, 0),
                'end_time': time(23, 0),
                'description': '血气流注于三焦，称手少阳三焦经。三焦通百脉，亥时三焦通百脉，人进入睡眠，百脉休养生息。',
                'health_tips': '尽量在21点至23点入睡，为身体充电。避免剧烈活动，保持安静的环境。',
                'case_suggestions': '失眠者应特别注意亥时的调养，可按摩三阴交穴、神门穴。睡前用热水泡脚，有助于入睡。',
                'food_recommendations': '睡前2小时内不宜进食。可饮用温牛奶或蜂蜜水，有助于安神入睡。'
            }
        ]

        for data in time_slots_data:
            time_slot, created = TimeSlot.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'创建时辰: {time_slot.chinese_name}')
            else:
                # 检查是否需要更新
                updated = False
                for field, value in data.items():
                    if field != 'name' and getattr(time_slot, field) != value:
                        setattr(time_slot, field, value)
                        updated = True
                
                if updated:
                    time_slot.save()
                    self.stdout.write(f'更新时辰: {time_slot.chinese_name}')
                else:
                    self.stdout.write(f'时辰未更新: {time_slot.chinese_name}')

    def init_acupoints(self):
        """初始化穴位数据"""
        acupoints_data = [
            {
                'name': '听宫',
                'body_part': 'ear',
                'location_description': '位于面部，耳屏前，下颌骨髁状突的后方，张口时呈凹陷处。',
                'massage_method': '用双手食指或中指指腹，轻柔地按压听宫穴，每次按压3-5秒，重复10-15次。按压时感到轻微酸胀感为宜。',
                'benefits': '主治耳鸣、耳聋、听力减退等耳部疾病。能够疏通耳部经络，改善局部血液循环。',
                'image': 'acupoints/tingong.jpg'
            },
            {
                'name': '翳风',
                'body_part': 'ear',
                'location_description': '位于耳垂后方，乳突与下颌骨之间的凹陷处。',
                'massage_method': '用拇指或食指指腹，垂直按压翳风穴，力度适中，每次按压3-5秒，重复10-15次。',
                'benefits': '治疗耳鸣、耳痛、面瘫等。有疏风解表、通利耳窍的作用。',
                'image': 'acupoints/yifeng.jpg'
            },
            {
                'name': '耳门',
                'body_part': 'ear',
                'location_description': '位于面部，耳屏上切迹的前方，下颌骨髁状突的后缘，张口时呈凹陷处。',
                'massage_method': '用食指指腹轻柔按压，配合小幅度的环形按摩，每次按摩1-2分钟。',
                'benefits': '主治耳鸣、耳聋、耳痛等耳部疾病。能够开窍聪耳，疏通经络。',
                'image': 'acupoints/ermen.jpg'
            },
            {
                'name': '百会',
                'body_part': 'head',
                'location_description': '位于头顶正中央，两耳尖连线与鼻梁中线的交叉点。',
                'massage_method': '用中指指腹垂直按压，或用手掌轻抚按摩，每次按压10-20秒，重复5-10次。',
                'benefits': '调节大脑功能，改善头部血液循环，对耳鸣、头痛、失眠有良好效果。',
                'image': 'acupoints/baihui.jpg'
            },
            {
                'name': '风池',
                'body_part': 'neck',
                'location_description': '位于颈部，枕骨之下，胸锁乳突肌与斜方肌上端之间的凹陷处。',
                'massage_method': '用双手拇指指腹，从下向上按压风池穴，力度适中，每次按压5-10秒，重复10次。',
                'benefits': '疏风解表，通利官窍。对头痛、颈椎病引起的耳鸣有很好的缓解作用。',
                'image': 'acupoints/fengchi.jpg'
            },
            {
                'name': '太冲',
                'body_part': 'foot',
                'location_description': '位于足背，第一、二跖骨结合部之前的凹陷处。',
                'massage_method': '用拇指指腹垂直按压，力度由轻到重，每次按压3-5秒，重复15-20次。',
                'benefits': '疏肝解郁，平肝潜阳。对肝火旺盛引起的耳鸣、头痛、急躁易怒有良好效果。',
                'image': 'acupoints/taichong.jpg'
            },
            {
                'name': '涌泉',
                'body_part': 'foot',
                'location_description': '位于足底，足前部凹陷处，约当足底2、3趾趾缝头端与足跟连线的前1/3与后2/3交点上。',
                'massage_method': '用拇指指腹用力按压，或用拳头敲击，每次按压10-15秒，重复10-15次。',
                'benefits': '补肾固本，引火归元。对肾虚引起的耳鸣、失眠、腰膝酸软有很好的调理作用。',
                'image': 'acupoints/yongquan.jpg'
            },
            {
                'name': '神门',
                'body_part': 'hand',
                'location_description': '位于腕部，腕掌侧横纹尺侧端，尺侧腕屈肌腱的桡侧凹陷处。',
                'massage_method': '用拇指指腹轻柔按压，配合小幅度的揉动，每次按摩2-3分钟。',
                'benefits': '安神定志，清心除烦。对心神不宁引起的耳鸣、失眠、健忘有良好效果。',
                'image': 'acupoints/shenmen.jpg'
            }
        ]

        for data in acupoints_data:
            acupoint, created = AcupointMassage.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'创建穴位: {acupoint.name}')
            else:
                # 检查是否需要更新
                updated = False
                for field, value in data.items():
                    if field != 'name' and getattr(acupoint, field) != value:
                        setattr(acupoint, field, value)
                        updated = True
                
                if updated:
                    acupoint.save()
                    self.stdout.write(f'更新穴位: {acupoint.name}')
                else:
                    self.stdout.write(f'穴位未更新: {acupoint.name}')